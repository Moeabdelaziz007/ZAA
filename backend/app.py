from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import os
from datetime import datetime, timedelta
import json
from zero_system import ZeroSystem
import hashlib
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cache import CacheMiddleware
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket
import time
from .api.routes import router
from .utils.config import settings
import asyncio
from typing import List, Dict
import logging
from prometheus_client import Counter, Histogram
import uvicorn
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['method', 'endpoint'])
AI_REQUEST_LATENCY = Histogram('ai_request_duration_seconds', 'AI request latency', ['model', 'operation'])

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_metrics = Counter('websocket_connections_total', 'Total WebSocket connections')
        self.message_metrics = Counter('websocket_messages_total', 'Total WebSocket messages')

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_metrics.inc()

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        self.message_metrics.inc()
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up application...")
    yield
    # Shutdown
    logger.info("Shutting down application...")

app = FastAPI(
    title="Zentix AI API",
    description="AI-powered recommendation system API",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(CacheMiddleware, cache_timeout=60)

# Performance monitoring middleware
@app.middleware("http")
async def performance_monitoring(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(process_time)
    
    response.headers["X-Process-Time"] = str(process_time)
    return response

# AI request optimization
async def optimize_ai_request(model: str, operation: str, request_func):
    start_time = time.time()
    try:
        result = await request_func()
        AI_REQUEST_LATENCY.labels(model=model, operation=operation).observe(time.time() - start_time)
        return result
    except Exception as e:
        logger.error(f"AI request failed: {str(e)}")
        raise

# WebSocket endpoints
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Process AI request with optimization
            result = await optimize_ai_request(
                model="recommendation",
                operation="realtime",
                request_func=lambda: process_realtime_recommendation(data)
            )
            await manager.broadcast(result)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        manager.disconnect(websocket)

# Health check endpoint
@app.get("/health")
async def health_check():
    return JSONResponse(
        content={"status": "healthy"},
        status_code=200
    )

# AI endpoints with optimization
@app.post("/api/v1/recommendations/")
async def get_recommendations(request: Request):
    return await optimize_ai_request(
        model="recommendation",
        operation="batch",
        request_func=lambda: process_batch_recommendation(request)
    )

@app.post("/api/v1/ai/analyze")
async def analyze_content(request: Request):
    return await optimize_ai_request(
        model="analysis",
        operation="content",
        request_func=lambda: process_content_analysis(request)
    )

# Helper functions
async def process_realtime_recommendation(data: str) -> str:
    # Implement real-time recommendation logic
    await asyncio.sleep(0.1)  # Simulate AI processing
    return f"Processed recommendation for: {data}"

async def process_batch_recommendation(request: Request) -> Dict:
    # Implement batch recommendation logic
    await asyncio.sleep(0.5)  # Simulate AI processing
    return {"recommendations": ["item1", "item2", "item3"]}

async def process_content_analysis(request: Request) -> Dict:
    # Implement content analysis logic
    await asyncio.sleep(0.3)  # Simulate AI processing
    return {"analysis": "Content analyzed successfully"}

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        workers=4,
        loop="uvloop",
        http="httptools",
        reload=True
    ) 