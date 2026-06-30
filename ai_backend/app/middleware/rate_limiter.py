"""Rate limiting middleware using slowapi."""

from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# NOTE: Known trade-off for hackathon -- get_remote_address resolves to the
# reverse proxy (PHP container) IP in the docker-compose topology, so all users
# share a single rate-limit bucket. In production, configure slowapi to use
# X-Forwarded-For or X-Real-IP with trusted proxy settings.
limiter = Limiter(key_func=get_remote_address)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Custom handler for rate limit exceeded errors."""
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "error": "Rate limit exceeded",
            "detail": str(exc.detail),
        },
    )
