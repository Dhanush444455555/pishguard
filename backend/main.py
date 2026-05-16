"""
PhishGuard AI — Enterprise Threat Intelligence Platform
=======================================================
FastAPI application entry point.

Engines:
  • Hindsight Memory    — Persistent threat memory & similarity matching
  • CascadeFlow Routing       — Intelligent 3-tier model routing
  • ML Ensemble Engine      — Weighted heuristic + statistical scoring
  • AI Reasoning Engine     — Chain-of-thought threat analysis
  • Explainable AI Engine   — Structured explainability reports
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from core.config import settings
from core.logger import logger
from core.exceptions import PhishGuardError, phishguard_exception_handler
from core.middleware import CorrelationIDMiddleware, RequestTimingMiddleware, RateLimitMiddleware
from routes.scan import router as scan_router
from routes.threat_history import router as history_router
from routes.system_status import router as status_router


# ── Lifecycle ─────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 60)
    logger.info(f"  {settings.PROJECT_NAME}")
    logger.info(f"  Version: {settings.VERSION}")
    logger.info(f"  Environment: {settings.APP_ENV}")
    logger.info(f"  API Prefix: {settings.API_V1_STR}")
    logger.info("=" * 60)
    logger.info("[Boot] Hindsight Memory ......... ONLINE")
    logger.info("[Boot] CascadeFlow Routing ............ ONLINE")
    logger.info("[Boot] ML Ensemble Engine ........... ONLINE")
    logger.info("[Boot] AI Reasoning Engine .......... ONLINE")
    logger.info("[Boot] Explainable AI Engine ........ ONLINE")
    logger.info("=" * 60)
    logger.info(f"  Docs:   http://localhost:8000/docs")
    logger.info(f"  ReDoc:  http://localhost:8000/redoc")
    logger.info(f"  Health: http://localhost:8000{settings.API_V1_STR}/system-status")
    logger.info("=" * 60)
    yield
    logger.info("[Shutdown] PhishGuard AI shutting down...")


# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "AI-powered phishing detection and cyber threat intelligence platform. "
        "Powered by Hindsight Memory and CascadeFlow Routing."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Scan", "description": "URL threat scanning and analysis"},
        {"name": "Threat Intelligence", "description": "Threat history and similarity search"},
        {"name": "System", "description": "Platform health and telemetry"},
    ],
)

# ── Exception Handlers ───────────────────────────────────────────────────────
app.add_exception_handler(PhishGuardError, phishguard_exception_handler)

# ── Middleware (order matters — outermost first) ──────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list if settings.is_production else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestTimingMiddleware)
app.add_middleware(CorrelationIDMiddleware)
app.add_middleware(
    RateLimitMiddleware,
    max_requests=settings.RATE_LIMIT_REQUESTS,
    window_seconds=settings.RATE_LIMIT_WINDOW_SECONDS,
)

# ── Routes ────────────────────────────────────────────────────────────────────
API = settings.API_V1_STR

app.include_router(scan_router, prefix=API, tags=["Scan"])
app.include_router(history_router, prefix=API, tags=["Threat Intelligence"])
app.include_router(status_router, prefix=API, tags=["System"])


# ── Root ──────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"], summary="Platform info")
async def root():
    return {
        "platform": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "engines": {
            "sentinel_memory_core": "Persistent threat memory & similarity matching",
            "neuralflow_router": "Intelligent 3-tier model routing",
            "ml_ensemble": "Weighted heuristic + statistical scoring",
            "ai_reasoning": "Chain-of-thought threat analysis",
            "explainable_ai": "Structured explainability reports",
        },
        "endpoints": {
            "scan": f"{API}/scan",
            "threat_history": f"{API}/threat-history",
            "similar_threats": f"{API}/similar-threats",
            "system_status": f"{API}/system-status",
            "docs": "/docs",
        },
    }
