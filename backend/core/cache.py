"""
نظام التخزين المؤقت الذكي
"""
from typing import Any, Optional, Callable
from functools import wraps
import json
from datetime import datetime, timedelta
import hashlib

from redis import Redis
from core.config import settings
from utils.logger import logger

class SmartCache:
    """مدير التخزين المؤقت الذكي"""
    
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.default_ttl = 300  # 5 دقائق
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """توليد مفتاح فريد للتخزين المؤقت"""
        # دمج المعاملات
        key_parts = [prefix]
        if args:
            key_parts.extend([str(arg) for arg in args])
        if kwargs:
            key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
        
        # إنشاء هاش
        key_string = ":".join(key_parts)
        return f"cache:{hashlib.md5(key_string.encode()).hexdigest()}"
    
    def get(self, key: str) -> Optional[Any]:
        """الحصول على قيمة من التخزين المؤقت"""
        try:
            data = self.redis.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.log_error(e, {"cache_key": key})
            return None
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """تخزين قيمة في التخزين المؤقت"""
        try:
            self.redis.setex(
                key,
                ttl or self.default_ttl,
                json.dumps(value)
            )
            return True
        except Exception as e:
            logger.log_error(e, {
                "cache_key": key,
                "ttl": ttl
            })
            return False
    
    def delete(self, key: str) -> bool:
        """حذف قيمة من التخزين المؤقت"""
        try:
            self.redis.delete(key)
            return True
        except Exception as e:
            logger.log_error(e, {"cache_key": key})
            return False
    
    def clear_pattern(self, pattern: str) -> bool:
        """حذف جميع القيم التي تطابق النمط"""
        try:
            keys = self.redis.keys(f"cache:{pattern}")
            if keys:
                self.redis.delete(*keys)
            return True
        except Exception as e:
            logger.log_error(e, {"pattern": pattern})
            return False
    
    def cached(
        self,
        prefix: str,
        ttl: Optional[int] = None,
        key_builder: Optional[Callable] = None
    ):
        """مزخرف للوظائف مع التخزين المؤقت"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # توليد المفتاح
                if key_builder:
                    cache_key = key_builder(*args, **kwargs)
                else:
                    cache_key = self._generate_key(prefix, *args, **kwargs)
                
                # محاولة الحصول من التخزين المؤقت
                cached_value = self.get(cache_key)
                if cached_value is not None:
                    logger.log_request(
                        method="CACHE",
                        endpoint=func.__name__,
                        status=200,
                        duration=0.0,
                        extra={"cache_hit": True}
                    )
                    return cached_value
                
                # تنفيذ الوظيفة
                result = await func(*args, **kwargs)
                
                # تخزين النتيجة
                self.set(cache_key, result, ttl)
                
                logger.log_request(
                    method="CACHE",
                    endpoint=func.__name__,
                    status=200,
                    duration=0.0,
                    extra={"cache_hit": False}
                )
                
                return result
            return wrapper
        return decorator

# إنشاء مثيل المدير
cache = SmartCache(settings.redis_client)
