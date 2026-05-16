"""
models/api_schemas.py — Enterprise Pydantic v2 schemas for PhishGuard AI.
Defines every request, response, and internal data model used across the platform.
"""

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


# ══════════════════════════════════════════════════════════════════════════════
#  Enums
# ══════════════════════════════════════════════════════════════════════════════

class ThreatLevel(str, Enum):
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RoutingTier(str, Enum):
    FAST = "fast"
    STANDARD = "standard"
    DEEP = "deep"


# ══════════════════════════════════════════════════════════════════════════════
#  Request Models
# ══════════════════════════════════════════════════════════════════════════════

class ScanRequest(BaseModel):
    """Request body for POST /scan."""
    url: str = Field(..., min_length=3, max_length=2048, description="URL to analyze for phishing threats")
    deep_scan: bool = Field(default=False, description="Force deep-tier analysis")

    model_config = {"json_schema_extra": {"examples": [{"url": "https://paypal-security-alert.xyz/login", "deep_scan": False}]}}


class SimilarThreatQuery(BaseModel):
    """Query parameters for GET /similar-threats."""
    url: str = Field(..., min_length=3, description="URL to find similar threats for")
    limit: int = Field(default=10, ge=1, le=50, description="Max results to return")
    threshold: float = Field(default=0.5, ge=0.0, le=1.0, description="Minimum similarity score")


# ══════════════════════════════════════════════════════════════════════════════
#  Internal / Component Models
# ══════════════════════════════════════════════════════════════════════════════

class AnomalyDetail(BaseModel):
    """A single anomaly detected during URL analysis."""
    title: str
    description: str
    impact: Severity
    category: str = Field(default="general", description="Anomaly category: structural, brand, protocol, obfuscation")


class URLFeatureSet(BaseModel):
    """Extracted numeric and boolean features from a URL."""
    url_length: int = 0
    domain: str = ""
    tld: str = ""
    has_https: bool = False
    is_safe_domain: bool = False
    brand_count: int = 0
    domain_entropy: float = 0.0
    path_entropy: float = 0.0
    digit_count: int = 0
    hyphen_count: int = 0
    subdomain_depth: int = 0
    path_depth: int = 0
    query_param_count: int = 0
    has_ip: bool = False
    has_at_symbol: bool = False
    has_port: bool = False
    is_suspicious_tld: bool = False


class ScoreContribution(BaseModel):
    """Breakdown of how a single feature contributes to the phishing score."""
    feature: str
    weight: float
    triggered: bool
    description: str


class KeywordAnalysisResult(BaseModel):
    """Result of suspicious keyword analysis."""
    keyword: str
    category: str  # "credential", "urgency", "brand", "financial"
    severity: Severity
    context: str  # where in the URL it was found


class RedirectChainEntry(BaseModel):
    """One hop in a detected redirect chain."""
    url: str
    status_hint: str  # "redirect_pattern", "obfuscated_path", etc.
    suspicious: bool


class ThreatIndicator(BaseModel):
    """A structured threat indicator for the explainability report."""
    indicator_type: str  # "structural", "behavioral", "brand_impersonation", "obfuscation"
    description: str
    severity: Severity
    evidence: str


class ZeroDayAssessment(BaseModel):
    """Zero-day threat probability assessment."""
    probability: float = Field(ge=0.0, le=1.0)
    reasoning: str
    novel_indicators: List[str] = Field(default_factory=list)
    recommendation: str


class ThreatTimelineEntry(BaseModel):
    """Entry in the threat evolution timeline."""
    timestamp: str
    event: str
    threat_level: ThreatLevel
    details: str


# ══════════════════════════════════════════════════════════════════════════════
#  Memory / Similarity Models
# ══════════════════════════════════════════════════════════════════════════════

class MemoryRecord(BaseModel):
    """A single record stored in the Hindsight Memory."""
    id: str
    url: str
    domain: str
    risk_score: int
    threat_level: ThreatLevel
    confidence: float
    scanned_at: str
    relative_time: str
    anomaly_count: int
    feature_vector: Optional[List[float]] = None


class SimilarThreat(BaseModel):
    """A similar threat found in the Hindsight Memory."""
    url: str
    domain: str
    similarity_score: float
    match_reasons: List[str]
    threat_level: ThreatLevel
    risk_score: int
    scanned_at: str


# ══════════════════════════════════════════════════════════════════════════════
#  AI / Reasoning Models
# ══════════════════════════════════════════════════════════════════════════════

class RoutingDecision(BaseModel):
    """CascadeFlow Routing's tier selection rationale."""
    selected_tier: RoutingTier
    tier_name: str
    reason: str
    complexity_score: float
    fallback_used: bool = False


class ExplainableReport(BaseModel):
    """Full explainability report generated by the AI engine."""
    summary: str
    reasoning_chain: List[str]
    risk_factors: List[ThreatIndicator]
    score_breakdown: List[ScoreContribution]
    zero_day_assessment: ZeroDayAssessment
    keyword_analysis: List[KeywordAnalysisResult]
    redirect_chain: List[RedirectChainEntry]
    recommendations: List[str]
    confidence_explanation: str


# ══════════════════════════════════════════════════════════════════════════════
#  Response Models
# ══════════════════════════════════════════════════════════════════════════════

class ScanResponse(BaseModel):
    """Complete response for POST /scan."""
    # ── Core result ─────────────────────────────────────────────────────
    url: str
    threat_level: ThreatLevel
    risk_score: int = Field(ge=0, le=100)
    confidence: float = Field(ge=0.0, le=100.0)
    is_phishing: bool

    # ── Features & anomalies ────────────────────────────────────────────
    features: URLFeatureSet
    anomalies: List[AnomalyDetail]

    # ── AI analysis ─────────────────────────────────────────────────────
    explainability: ExplainableReport
    routing: RoutingDecision

    # ── Memory context ──────────────────────────────────────────────────
    similar_threats: List[SimilarThreat]
    threat_timeline: List[ThreatTimelineEntry]

    # ── Metadata ────────────────────────────────────────────────────────
    scan_id: str
    latency_ms: float
    engine_version: str
    timestamp: str


class ThreatHistoryResponse(BaseModel):
    """Response for GET /threat-history."""
    total_records: int
    records: List[MemoryRecord]
    stats: Dict[str, Any]


class SimilarThreatResponse(BaseModel):
    """Response for GET /similar-threats."""
    query_url: str
    total_matches: int
    matches: List[SimilarThreat]


class EngineStatus(BaseModel):
    """Status of a single engine component."""
    name: str
    status: str  # "operational", "degraded", "offline"
    version: str
    uptime_seconds: float
    metrics: Dict[str, Any] = Field(default_factory=dict)


class SystemStatusResponse(BaseModel):
    """Response for GET /system-status."""
    status: str  # "operational", "degraded"
    version: str
    project: str
    uptime_seconds: float
    engines: Dict[str, EngineStatus]
    scan_metrics: Dict[str, Any]
    memory_metrics: Dict[str, Any]
