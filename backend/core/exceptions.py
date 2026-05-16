"""
core/exceptions.py — Custom exception hierarchy for PhishGuard AI.
Provides structured error responses across all API endpoints.
"""

from fastapi import Request
from fastapi.responses import JSONResponse


# ── Base Exception ────────────────────────────────────────────────────────────
class PhishGuardError(Exception):
    """Base exception for all PhishGuard AI errors."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


# ── Specific Exceptions ──────────────────────────────────────────────────────
class ScanError(PhishGuardError):
    """Raised when a URL scan operation fails."""

    def __init__(self, message: str = "URL scan failed"):
        super().__init__(message=message, code="SCAN_ERROR", status_code=422)


class InvalidURLError(PhishGuardError):
    """Raised when an input URL is malformed or invalid."""

    def __init__(self, url: str = ""):
        super().__init__(
            message=f"Invalid or malformed URL: {url}",
            code="INVALID_URL",
            status_code=422,
        )


class MemoryEngineError(PhishGuardError):
    """Raised when Hindsight Memory encounters an error."""

    def __init__(self, message: str = "Hindsight Memory encountered an error"):
        super().__init__(message=message, code="MEMORY_ENGINE_ERROR", status_code=500)


class RoutingError(PhishGuardError):
    """Raised when CascadeFlow Routing fails to select or execute a tier."""

    def __init__(self, message: str = "CascadeFlow Routing encountered a routing error"):
        super().__init__(message=message, code="ROUTING_ERROR", status_code=500)


class RateLimitError(PhishGuardError):
    """Raised when a client exceeds the request rate limit."""

    def __init__(self, message: str = "Rate limit exceeded. Please try again later."):
        super().__init__(message=message, code="RATE_LIMIT_EXCEEDED", status_code=429)


class ReasoningError(PhishGuardError):
    """Raised when the AI reasoning engine fails."""

    def __init__(self, message: str = "AI reasoning engine encountered an error"):
        super().__init__(message=message, code="REASONING_ERROR", status_code=500)


# ── FastAPI Exception Handlers ────────────────────────────────────────────────
async def phishguard_exception_handler(request: Request, exc: PhishGuardError):
    """Global handler that converts PhishGuardError subclasses to structured JSON."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "code": exc.code,
            "message": exc.message,
            "detail": str(exc),
            "path": str(request.url),
        },
    )
