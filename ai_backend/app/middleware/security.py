"""Security headers middleware."""

from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Paths that serve interactive documentation (Swagger UI, ReDoc) load external
# JS/CSS from CDN, so a strict CSP would break them.
_DOCS_PATHS = ("/docs", "/redoc", "/openapi.json")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to every response."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Skip strict CSP for documentation paths to allow Swagger UI/ReDoc
        # to load their JS/CSS bundles from CDN.
        if not request.url.path.startswith(_DOCS_PATHS):
            response.headers["Content-Security-Policy"] = "default-src 'self'"

        return response
