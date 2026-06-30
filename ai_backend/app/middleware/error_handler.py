"""Global exception handler with graceful degradation.

NOTE: This handler is NOT registered as an app-level exception handler because
the StructuredLoggingMiddleware already catches all unhandled exceptions higher
in the Starlette stack. This module is kept as a reference implementation of the
consistent error response format and can be used if the middleware architecture
changes in the future.
"""

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
