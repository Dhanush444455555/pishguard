"""
routes/scan.py — POST /api/v1/scan
Accepts a URL, runs it through the full PhishGuard analysis pipeline,
and returns structured threat intelligence.
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from ai.agent import agent
from utils.url_parser import is_valid_url
from utils.logger import log_scan_event, log_threat_detected
from core.logger import logger

router = APIRouter()


class ScanRequest(BaseModel):
    url: str = Field(..., min_length=3, max_length=2048, description="URL to scan")
    deep_scan: bool = Field(default=False, description="Force deep-tier analysis")


@router.post("/scan", summary="Scan URL for phishing threats",
             description="Submit a URL for comprehensive AI-powered threat analysis")
async def scan_url(body: ScanRequest, request: Request):
    """
    Full PhishGuard scan pipeline:
    1. CascadeFlow Routing selects analysis tier
    2. URL features extracted
    3. ML ensemble scoring
    4. Hindsight Memory lookup
    5. AI reasoning engine
    6. Explainable report generation
    """
    url = body.url.strip()

    if not url:
        raise HTTPException(status_code=422, detail="URL must not be empty.")

    # Ensure scheme
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    if not is_valid_url(url):
        raise HTTPException(status_code=422, detail=f"Invalid URL: {url}")

    try:
        result = await agent.analyze(url, force_deep=body.deep_scan)
    except Exception as e:
        logger.error(f"Scan failed for {url[:60]}: {e}")
        raise HTTPException(status_code=500, detail="Scan pipeline error")

    # Audit logging
    client_ip = request.client.host if request.client else "unknown"
    log_scan_event(
        scan_id=result["scan_id"],
        url=url,
        risk_score=result["risk_score"],
        threat_level=result["threat_level"],
        latency_ms=result["latency_ms"],
        routing_tier=result["routing"]["selected_tier"],
        client_ip=client_ip,
    )
    log_threat_detected(
        scan_id=result["scan_id"],
        url=url,
        risk_score=result["risk_score"],
        anomaly_count=len(result["anomalies"]),
    )

    return result
