"""
utils/logger.py — Audit logging utilities for PhishGuard AI.
Provides structured scan event logging for compliance and security monitoring.
"""

from datetime import datetime, timezone
from core.logger import audit_logger


def log_scan_event(
    scan_id: str,
    url: str,
    risk_score: int,
    threat_level: str,
    latency_ms: float,
    routing_tier: str,
    client_ip: str = "unknown",
) -> None:
    """
    Log a scan event to the security audit trail.

    Args:
        scan_id: Unique scan identifier.
        url: The scanned URL (will be partially masked).
        risk_score: Computed risk score (0-100).
        threat_level: Determined threat level.
        latency_ms: Scan processing time in milliseconds.
        routing_tier: CascadeFlow Routing tier used.
        client_ip: Client IP address (for rate tracking).
    """
    # Mask the URL for log safety (show domain only)
    masked = _mask_url(url)

    audit_logger.info(
        f"SCAN_EVENT | id={scan_id} | url={masked} | "
        f"risk={risk_score} | level={threat_level} | "
        f"tier={routing_tier} | latency={latency_ms}ms | "
        f"client={client_ip} | ts={datetime.now(timezone.utc).isoformat()}"
    )


def log_threat_detected(
    scan_id: str,
    url: str,
    risk_score: int,
    anomaly_count: int,
) -> None:
    """Log a high-risk threat detection event."""
    if risk_score >= 65:
        audit_logger.warning(
            f"THREAT_DETECTED | id={scan_id} | url={_mask_url(url)} | "
            f"risk={risk_score} | anomalies={anomaly_count}"
        )


def log_memory_event(action: str, url: str, details: str = "") -> None:
    """Log a Hindsight Memory event."""
    audit_logger.info(
        f"MEMORY_EVENT | action={action} | url={_mask_url(url)} | {details}"
    )


def _mask_url(url: str) -> str:
    """Partially mask a URL for safe logging — show domain, truncate path."""
    from urllib.parse import urlparse
    try:
        parsed = urlparse(url if "://" in url else f"https://{url}")
        domain = parsed.hostname or "unknown"
        path = parsed.path[:30] + "..." if len(parsed.path) > 30 else parsed.path
        return f"{parsed.scheme}://{domain}{path}"
    except Exception:
        return url[:50] + "..." if len(url) > 50 else url
