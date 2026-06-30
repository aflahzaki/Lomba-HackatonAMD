"""Global exception handler with graceful degradation."""

from datetime import datetime

from fastapi import Request
from fastapi.responses import JSONResponse


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch all unhandled exceptions and return a consistent JSON error response."""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": type(exc).__name__,
            "detail": str(exc) if str(exc) else "An unexpected error occurred",
            "timestamp": datetime.now().isoformat(),
        },
    )
