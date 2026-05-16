"""
ai/agent.py — PhishGuard Agent: Top-level orchestrator for PhishGuard AI.
Coordinates the full scan pipeline:
  Feature Extraction → ML Prediction → Memory Lookup →
  AI Reasoning → Explainability → Memory Storage
"""

import time
import uuid
from datetime import datetime, timezone

from services.url_analyzer import extract_features
from services.ml_predictor import predict
from services.sentinel_memory import memory_store
from services.neuralflow_router import router as neuralflow_router
from services.threat_explainer import explainer_engine
from ai.reasoning import reasoning_engine
from utils.feature_extractor import features_to_vector
from utils.url_parser import normalize_url
from core.logger import logger


class PhishGuardAgent:
    """
    Top-level orchestrator that runs the complete threat analysis pipeline.
    Returns a unified ScanResponse-compatible dict.
    """

    def __init__(self):
        self._scan_count = 0
        logger.info("[PhishGuard Agent] Initialized — all engines online")

    async def analyze(self, url: str, force_deep: bool = False) -> dict:
        """
        Full async scan pipeline.

        Args:
            url: The URL to analyze.
            force_deep: Force deep-tier analysis regardless of complexity.

        Returns:
            Complete scan result dict matching ScanResponse schema.
        """
        start = time.perf_counter()
        scan_id = str(uuid.uuid4())[:12]
        self._scan_count += 1

        # Normalize URL
        normalized = normalize_url(url)

        # ── Step 1: CascadeFlow Routing ────────────────────────────────────
        routing = neuralflow_router.select_tier(normalized, force_deep=force_deep)
        tier = routing["selected_tier"]

        # ── Step 2: Feature Extraction ────────────────────────────────────
        features = extract_features(normalized)

        # ── Step 3: ML Prediction ─────────────────────────────────────────
        prediction = predict(features)

        # ── Step 4: Memory Lookup (standard & deep tiers) ─────────────────
        similar_threats = []
        threat_timeline = []
        if tier in ("standard", "deep"):
            fv = features_to_vector(features)
            similar_threats = memory_store.find_similar(fv, limit=5, threshold=0.5)
            threat_timeline = memory_store.get_threat_timeline(features.domain)

        # ── Step 5: AI Reasoning (deep tier only) ─────────────────────────
        if tier == "deep":
            reasoning_result = reasoning_engine.reason(
                features, prediction, similar_threats
            )
        else:
            reasoning_result = self._quick_reasoning(features, prediction)

        # ── Step 6: Explainability Report ─────────────────────────────────
        explainability = explainer_engine.explain(
            features, prediction, reasoning_result, similar_threats
        )

        # ── Step 7: Record in Hindsight Memory ─────────────────────────────
        memory_store.record_scan(normalized, features, prediction)

        # ── Step 8: Compute latency & record telemetry ────────────────────
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        neuralflow_router.record_latency(tier, elapsed_ms)

        # ── Build feature summary for response ────────────────────────────
        feature_summary = {
            "url_length": features.url_length,
            "domain": features.domain,
            "tld": features.tld,
            "has_https": features.has_https,
            "is_safe_domain": features.is_safe_domain,
            "brand_count": features.brand_count,
            "domain_entropy": round(features.domain_entropy, 3),
            "path_entropy": round(features.path_entropy, 3),
            "digit_count": features.digit_count,
            "hyphen_count": features.hyphen_count,
            "subdomain_depth": features.subdomain_depth,
            "path_depth": features.path_depth,
            "query_param_count": features.query_param_count,
            "has_ip": features.has_ip,
            "has_at_symbol": features.has_at_symbol,
            "has_port": features.has_port,
            "is_suspicious_tld": features.is_suspicious_tld,
        }

        # ── Format anomalies ──────────────────────────────────────────────
        anomalies = [
            {
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "impact": a.get("impact", "medium"),
                "category": a.get("category", "general"),
            }
            for a in features.anomalies
        ]

        # ── Routing decision ──────────────────────────────────────────────
        routing_decision = {
            "selected_tier": routing["selected_tier"],
            "tier_name": routing["tier_name"],
            "reason": routing["reason"],
            "complexity_score": routing["complexity_score"],
            "fallback_used": routing["fallback_used"],
        }

        risk_score = prediction["probability"]

        return {
            "url": normalized,
            "threat_level": prediction["threat_level"],
            "risk_score": risk_score,
            "confidence": prediction["confidence"],
            "is_phishing": risk_score >= 55,
            "features": feature_summary,
            "anomalies": anomalies,
            "explainability": explainability,
            "routing": routing_decision,
            "similar_threats": similar_threats,
            "threat_timeline": threat_timeline,
            "scan_id": scan_id,
            "latency_ms": elapsed_ms,
            "engine_version": "PhishGuard-AI v2.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def _quick_reasoning(self, features, prediction: dict) -> dict:
        """Lightweight reasoning for fast/standard tiers."""
        threat_level = prediction.get("threat_level", "medium")
        risk_score = prediction.get("probability", 0)
        anomaly_count = len(features.anomalies)

        if features.is_safe_domain:
            summary = f"✅ SAFE — Known legitimate domain ({features.domain}). No anomalies detected."
        elif risk_score >= 55:
            summary = f"🔴 HIGH RISK — {anomaly_count} anomalies detected. Risk score: {risk_score}/100."
        elif risk_score >= 30:
            summary = f"🟡 MODERATE RISK — Some suspicious patterns found. Risk score: {risk_score}/100."
        else:
            summary = f"🟢 LOW RISK — Minimal suspicious indicators. Risk score: {risk_score}/100."

        from ai.prompts import get_recommendations
        return {
            "summary": summary,
            "reasoning_chain": [
                f"Quick-scan mode ({prediction.get('model_used', 'heuristic')})",
                f"Extracted features and scored {risk_score}/100",
                f"Detected {anomaly_count} anomalies",
            ],
            "recommendations": get_recommendations(threat_level),
            "confidence_explanation": f"Quick-scan confidence: {prediction.get('confidence', 0)}%",
        }

    @property
    def scan_count(self) -> int:
        return self._scan_count


# ── Singleton ─────────────────────────────────────────────────────────────────
agent = PhishGuardAgent()
