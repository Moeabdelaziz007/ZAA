"""
وسيط التحقق من الصلاحيات
"""
from typing import Callable, Optional
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta

from core.config import settings
from core.security import verify_token
from models.user import User
from utils.logger import logger

security = HTTPBearer()

class AuthMiddleware:
    """وسيط التحقق من الصلاحيات"""
    
    def __init__(self, required_roles: Optional[list] = None):
        self.required_roles = required_roles or []
    
    async def __call__(
        self,
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> User:
        try:
            # التحقق من التوكن
            token = credentials.credentials
            payload = verify_token(token)
            
            if not payload:
                raise HTTPException(
                    status_code=401,
                    detail="توكن غير صالح"
                )
            
            # التحقق من انتهاء الصلاحية
            exp = payload.get("exp")
            if not exp or datetime.fromtimestamp(exp) < datetime.now():
                raise HTTPException(
                    status_code=401,
                    detail="انتهت صلاحية التوكن"
                )
            
            # الحصول على المستخدم
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=401,
                    detail="بيانات المستخدم غير صالحة"
                )
            
            # التحقق من الأدوار المطلوبة
            if self.required_roles:
                user_roles = payload.get("roles", [])
                if not any(role in user_roles for role in self.required_roles):
                    raise HTTPException(
                        status_code=403,
                        detail="غير مصرح لك بالوصول إلى هذا المورد"
                    )
            
            # تسجيل الطلب
            logger.log_request(
                method=request.method,
                endpoint=request.url.path,
                status=200,
                duration=0.0,
                extra={
                    "user_id": user_id,
                    "roles": payload.get("roles", [])
                }
            )
            
            return User(id=user_id, **payload)
            
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="توكن غير صالح"
            )
        except Exception as e:
            logger.log_error(e, {
                "method": request.method,
                "endpoint": request.url.path
            })
            raise HTTPException(
                status_code=500,
                detail="حدث خطأ أثناء التحقق من الصلاحيات"
            )

def require_auth(roles: Optional[list] = None) -> Callable:
    """دالة مساعدة للتحقق من الصلاحيات"""
    return AuthMiddleware(required_roles=roles) 