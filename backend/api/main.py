"""Main API router configuration for FastAPI app."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.cache import CacheMiddleware

from core.config import (
    PROJECT_NAME,
    DEBUG,
    CORS_ORIGINS,
    API_V1_PREFIX,
)

# Import routers
from .routes import (
    auth,
    users,
    items,
    recommendations,
    interactions,
)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=PROJECT_NAME,
        debug=DEBUG,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        CacheMiddleware,
        cache_control="max-age=3600",
        vary_on=["accept-encoding", "accept-language"],
    )

    # Include routers
    app.include_router(auth.router, prefix=f"{API_V1_PREFIX}/auth", tags=["Authentication"])
    app.include_router(users.router, prefix=f"{API_V1_PREFIX}/users", tags=["Users"])
    app.include_router(items.router, prefix=f"{API_V1_PREFIX}/items", tags=["Items"])
    app.include_router(
        recommendations.router,
        prefix=f"{API_V1_PREFIX}/recommendations",
        tags=["Recommendations"],
    )
    app.include_router(interactions.router, prefix=f"{API_V1_PREFIX}/interactions", tags=["Interactions"])

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy"}

    return app


app = create_app()
