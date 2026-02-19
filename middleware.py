"""
Request logging middleware: logs every API request to the logs table.
"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from database import SessionLocal
from models import Log

# Paths to skip logging (health, docs, static)
SKIP_LOG_PATHS = {"/health", "/", "/docs", "/redoc", "/openapi.json"}


async def log_request(request: Request, call_next):
    """Log request to DB after response is ready."""
    path = request.url.path
    if path in SKIP_LOG_PATHS:
        return await call_next(request)

    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = int((time.perf_counter() - start) * 1000)

    status_code = response.status_code
    if status_code >= 500:
        level = "error"
    elif status_code >= 400:
        level = "warning"
    else:
        level = "info"

    message = f"{request.method} {path} -> {status_code}"
    client_host = request.client.host if request.client else None
    forwarded = request.headers.get("x-forwarded-for")
    ip_address = forwarded.split(",")[0].strip() if forwarded else client_host

    db = SessionLocal()
    try:
        log = Log(
            level=level,
            message=message,
            endpoint=path,
            method=request.method,
            status_code=status_code,
            user_id=None,  # can be set by auth dependency if needed
            ip_address=ip_address,
            duration_ms=duration_ms,
        )
        db.add(log)
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

    return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        return await log_request(request, call_next)
