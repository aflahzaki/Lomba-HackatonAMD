"""Structured JSON logging middleware for request/response timing."""

import logging
import time
from datetime import datetime
from typing import Callable

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("langkahkampus.access")


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs each request with method, path, status code, and response time.

    Also acts as the global exception safety net, catching unhandled exceptions
    and returning a consistent JSON error response.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        try:
            response = await call_next(request)
        except Exception as exc:
            # Global exception handler: catch unhandled exceptions
            response_time_ms = round((time.time() - start_time) * 1000, 2)
            log_data = {
                "method": request.method,
                "path": request.url.path,
                "status_code": 500,
                "response_time_ms": response_time_ms,
            }
            logger.error(
                "%(method)s %(path)s %(status_code)s %(response_time_ms)sms [ERROR]",
                log_data,
            )
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": type(exc).__name__,
                    "detail": str(exc) if str(exc) else "An unexpected error occurred",
                    "timestamp": datetime.now().isoformat(),
                },
            )

        response_time_ms = round((time.time() - start_time) * 1000, 2)

        log_data = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "response_time_ms": response_time_ms,
        }

        logger.info(
            "%(method)s %(path)s %(status_code)s %(response_time_ms)sms",
            log_data,
        )

        return response
