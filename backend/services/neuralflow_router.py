"""
services/neuralflow_router.py — CascadeFlow Routing for PhishGuard AI.
Intelligent 3-tier model routing with automatic tier selection,
routing telemetry, fallback chains, and latency tracking.
"""

import time
from core.logger import logger


# ── Tier Definitions ──────────────────────────────────────────────────────────

TIERS = {
    "fast": {
        "name": "CascadeFlow-Fast (Heuristic-v1)",
        "description": "Instant heuristic scan — short, low-complexity URLs.",
        "model": "phishguard-heuristic-v1",
        "target_latency_ms": 10,
    },
    "standard": {
        "name": "CascadeFlow-Standard (Ensemble-v2)",
        "description": "Full feature extraction with weighted ensemble scoring.",
        "model": "phishguard-ensemble-v2",
        "target_latency_ms": 50,
    },
    "deep": {
        "name": "CascadeFlow-Deep (Ensemble-v3 + Reasoning)",
        "description": "Maximum scrutiny — full pipeline with AI reasoning and memory lookup.",
        "model": "phishguard-ensemble-v3",
        "target_latency_ms": 200,
    },
}


class CascadeFlowRouter:
    """Intelligent model routing engine that selects the optimal analysis tier."""

    def __init__(self):
        self._tier_counts = {"fast": 0, "standard": 0, "deep": 0}
        self._tier_latencies = {"fast": [], "standard": [], "deep": []}
        self._total_routed = 0
        logger.info("[CascadeFlow Routing] Initialized with 3 analysis tiers")

    def select_tier(self, url: str, force_deep: bool = False) -> dict:
        """
        Select the optimal analysis tier based on URL complexity signals.

        Returns routing decision with tier key, name, reason, and complexity score.
        """
        if force_deep:
            tier_key = "deep"
            reason = "Deep scan explicitly requested by user"
            complexity = 1.0
        else:
            complexity = self._compute_complexity(url)
            tier_key, reason = self._route_by_complexity(url, complexity)

        tier = TIERS[tier_key]
        self._tier_counts[tier_key] += 1
        self._total_routed += 1

        return {
            "selected_tier": tier_key,
            "tier_name": tier["name"],
            "reason": reason,
            "complexity_score": round(complexity, 3),
            "fallback_used": False,
            "model": tier["model"],
            "description": tier["description"],
        }

    def record_latency(self, tier_key: str, latency_ms: float):
        """Record latency for SLA monitoring."""
        if tier_key in self._tier_latencies:
            self._tier_latencies[tier_key].append(latency_ms)
            # Keep only last 100 measurements per tier
            if len(self._tier_latencies[tier_key]) > 100:
                self._tier_latencies[tier_key] = self._tier_latencies[tier_key][-100:]

    def get_telemetry(self) -> dict:
        """Return routing telemetry metrics."""
        avg_latencies = {}
        for tier, latencies in self._tier_latencies.items():
            if latencies:
                avg_latencies[tier] = round(sum(latencies) / len(latencies), 2)
            else:
                avg_latencies[tier] = 0.0

        return {
            "total_routed": self._total_routed,
            "tier_distribution": dict(self._tier_counts),
            "average_latencies_ms": avg_latencies,
            "tiers_available": list(TIERS.keys()),
        }

    def _compute_complexity(self, url: str) -> float:
        """Compute a 0-1 complexity score for routing decisions."""
        score = 0.0
        url_len = len(url)

        # Length contribution
        if url_len > 150:
            score += 0.25
        elif url_len > 80:
            score += 0.10

        # Encoding
        if "%" in url:
            score += 0.15
        if url.count("%") > 3:
            score += 0.10

        # @ symbol
        if "@" in url:
            score += 0.15

        # Deep path
        if url.count("/") > 5:
            score += 0.10

        # Query complexity
        if "?" in url and url.count("&") > 2:
            score += 0.05

        # Subdomain depth
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url if "://" in url else f"https://{url}")
            host = parsed.hostname or ""
            if host.count(".") > 3:
                score += 0.10
        except Exception:
            pass

        return min(score, 1.0)

    def _route_by_complexity(self, url: str, complexity: float):
        """Route based on complexity score with explanatory reason."""
        url_len = len(url)

        if complexity >= 0.4:
            return "deep", (
                f"High complexity ({complexity:.2f}) — "
                f"URL exhibits encoding, depth, or obfuscation signals"
            )
        elif url_len < 40 and complexity < 0.1:
            return "fast", (
                f"Low complexity ({complexity:.2f}) — "
                f"Short, simple URL with no suspicious patterns"
            )
        else:
            return "standard", (
                f"Moderate complexity ({complexity:.2f}) — "
                f"Standard analysis pipeline selected"
            )


# ── Singleton ─────────────────────────────────────────────────────────────────
router = CascadeFlowRouter()
