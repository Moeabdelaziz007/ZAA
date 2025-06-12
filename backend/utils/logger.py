"""
نظام تسجيل متقدم مع دعم Sentry و Prometheus
"""
import logging
import sys
from typing import Any, Dict, Optional
from datetime import datetime

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from prometheus_client import Counter, Histogram, Gauge
from prometheus_client.exposition import generate_latest

# تكوين Sentry
sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    integrations=[
        FastApiIntegration(),
        SqlalchemyIntegration(),
    ],
    traces_sample_rate=1.0,
    environment="development",
)

# مقاييس Prometheus
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

ERROR_COUNT = Counter(
    'http_errors_total',
    'Total HTTP errors',
    ['method', 'endpoint', 'error_type']
)

ACTIVE_USERS = Gauge(
    'active_users',
    'Number of active users'
)

class CustomFormatter(logging.Formatter):
    """تنسيق مخصص للسجلات"""
    
    def format(self, record: logging.LogRecord) -> str:
        # إضافة الطابع الزمني
        record.timestamp = datetime.fromtimestamp(record.created).isoformat()
        
        # إضافة معلومات إضافية
        if not hasattr(record, 'extra'):
            record.extra = {}
        
        # تنسيق الرسالة
        return super().format(record)

class AdvancedLogger:
    """مدير تسجيل متقدم"""
    
    def __init__(
        self,
        name: str,
        level: int = logging.INFO,
        log_file: Optional[str] = None
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # تنسيق السجلات
        formatter = CustomFormatter(
            '%(timestamp)s [%(levelname)s] %(name)s: %(message)s'
        )
        
        # إضافة معالج وحدة التحكم
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # إضافة معالج الملف إذا تم تحديده
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def log_request(
        self,
        method: str,
        endpoint: str,
        status: int,
        duration: float,
        extra: Optional[Dict[str, Any]] = None
    ):
        """تسجيل طلب HTTP"""
        # تحديث مقاييس Prometheus
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)
        
        # تسجيل في Sentry
        if status >= 400:
            sentry_sdk.capture_message(
                f"HTTP {status} on {method} {endpoint}",
                level="error",
                extra=extra
            )
        
        # تسجيل محلي
        self.logger.info(
            f"{method} {endpoint} - {status} ({duration:.2f}s)",
            extra=extra
        )
    
    def log_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ):
        """تسجيل خطأ"""
        # تحديث مقاييس Prometheus
        ERROR_COUNT.labels(
            method=context.get('method', 'unknown'),
            endpoint=context.get('endpoint', 'unknown'),
            error_type=type(error).__name__
        ).inc()
        
        # تسجيل في Sentry
        sentry_sdk.capture_exception(error)
        
        # تسجيل محلي
        self.logger.error(
            f"Error: {str(error)}",
            exc_info=True,
            extra=context
        )
    
    def log_user_activity(
        self,
        user_id: int,
        action: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """تسجيل نشاط المستخدم"""
        # تحديث مقاييس Prometheus
        ACTIVE_USERS.inc()
        
        # تسجيل محلي
        self.logger.info(
            f"User {user_id} performed {action}",
            extra={
                'user_id': user_id,
                'action': action,
                **details or {}
            }
        )
    
    def get_metrics(self) -> str:
        """الحصول على مقاييس Prometheus"""
        return generate_latest().decode('utf-8')

# إنشاء مثيل المدير
logger = AdvancedLogger(
    name="zentix",
    level=logging.INFO,
    log_file="logs/app.log"
)
