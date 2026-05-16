"""
core/middleware.py — ASGI middleware for PhishGuard AI.
Provides request timing, correlation IDs, and in-memory rate limiting.
"""

import time
import uuid
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from core.logger import logger


# ── Correlation ID Middleware ─────────────────────────────────────────────────
class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """
    Attaches a unique X-Request-ID to every request/response pair.
    If the client sends one, it is preserved; otherwise a UUID is generated.
    """

    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.correlation_id = correlation_id
        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = correlation_id
        return response


# ── Request Timing Middleware ─────────────────────────────────────────────────
class RequestTimingMiddleware(BaseHTTPMiddleware):
    """Measures request processing time and injects X-Process-Time header."""

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response: Response = await call_next(request)
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        response.headers["X-Process-Time"] = f"{elapsed_ms}ms"

        # Log slow requests
        if elapsed_ms > 500:
            logger.warning(
                f"Slow request: {request.method} {request.url.path} took {elapsed_ms}ms"
            )

        return response


# ── Rate Limiting Middleware ──────────────────────────────────────────────────
class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    In-memory token-bucket rate limiter per client IP.
    For production, replace with Redis-backed implementation.
    """

    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._buckets: dict = defaultdict(lambda: {"count": 0, "reset_at": 0.0})

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for docs and health endpoints
        if request.url.path in ("/docs", "/redoc", "/openapi.json", "/", "/api/v1/system-status"):
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        bucket = self._buckets[client_ip]

        # Reset bucket if window has expired
        if now > bucket["reset_at"]:
            bucket["count"] = 0
            bucket["reset_at"] = now + self.window_seconds

        bucket["count"] += 1

        if bucket["count"] > self.max_requests:
            remaining_seconds = int(bucket["reset_at"] - now)
            logger.warning(f"Rate limit exceeded for {client_ip}")
            return JSONResponse(
                status_code=429,
                content={
                    "error": True,
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": "Too many requests. Please try again later.",
                    "retry_after_seconds": remaining_seconds,
                },
                headers={"Retry-After": str(remaining_seconds)},
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(
            max(0, self.max_requests - bucket["count"])
        )
        return response
