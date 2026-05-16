"""
routes/system_status.py — GET /api/v1/system-status
Comprehensive system health, engine status, and telemetry.
"""

import time
from datetime import datetime, timezone
from fastapi import APIRouter

from core.config import settings
from services.sentinel_memory import memory_store
from services.neuralflow_router import router as neuralflow_router
from ai.agent import agent

router = APIRouter()

_boot_time = time.time()


@router.get("/system-status", summary="Platform health & telemetry",
            description="Comprehensive system status for PhishGuard AI")
async def system_status():
    """
    Returns full platform health including engine statuses,
    scan metrics, memory utilization, and routing telemetry.
    """
    uptime = round(time.time() - _boot_time, 1)
    memory_stats = memory_store.get_stats()
    routing_telemetry = neuralflow_router.get_telemetry()

    return {
        "status": "operational",
        "version": settings.VERSION,
        "project": settings.PROJECT_NAME,
        "uptime_seconds": uptime,
        "environment": settings.APP_ENV,
        "engines": {
            "sentinel_memory_core": {
                "name": "Hindsight Memory",
                "status": "operational",
                "version": "2.0.0",
                "uptime_seconds": memory_store.uptime_seconds,
                "metrics": {
                    "stored_records": memory_stats.get("stored_records", 0),
                    "memory_utilization": memory_stats.get("memory_utilization", 0),
                    "total_scans_processed": memory_stats.get("total_scans", 0),
                },
            },
            "neuralflow_router": {
                "name": "CascadeFlow Routing",
                "status": "operational",
                "version": "2.0.0",
                "uptime_seconds": uptime,
                "metrics": routing_telemetry,
            },
            "ml_ensemble": {
                "name": "ML Ensemble Engine",
                "status": "operational",
                "version": "Ensemble-v3",
                "uptime_seconds": uptime,
                "metrics": {
                    "models_loaded": 3,
                    "active_model": "PhishGuard-Ensemble-v3",
                },
            },
            "ai_reasoning": {
                "name": "AI Reasoning Engine",
                "status": "operational",
                "version": "2.0.0",
                "uptime_seconds": uptime,
                "metrics": {
                    "reasoning_mode": "chain-of-thought",
                    "template_count": 5,
                },
            },
        },
        "scan_metrics": {
            "total_scans": agent.scan_count,
            "average_risk": memory_stats.get("average_risk", 0),
            "high_risk_count": memory_stats.get("high_risk", 0),
            "safe_count": memory_stats.get("safe", 0),
            "threat_distribution": memory_stats.get("threat_distribution", {}),
        },
        "memory_metrics": {
            "stored_records": memory_stats.get("stored_records", 0),
            "memory_utilization_pct": memory_stats.get("memory_utilization", 0),
            "top_domains": memory_stats.get("top_domains", []),
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
