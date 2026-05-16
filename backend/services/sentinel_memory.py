"""
services/sentinel_memory.py — Hindsight Memory for PhishGuard AI.
Persistent threat memory with domain fingerprinting, similarity matching,
threat timeline generation, adaptive learning, and campaign clustering.
"""

import uuid
import math
from collections import deque
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from dataclasses import asdict

from core.logger import logger
from utils.feature_extractor import features_to_vector


MAX_MEMORY = 10000


class ThreatMemoryStore:
    """
    In-memory threat intelligence store with persistence-ready architecture.
    Stores scan results with feature vectors for similarity search.
    """

    def __init__(self):
        self._records: deque = deque(maxlen=MAX_MEMORY)
        self._domain_index: Dict[str, List[str]] = {}  # domain -> [record_ids]
        self._scan_count: int = 0
        self._started_at: datetime = datetime.now(timezone.utc)
        logger.info("[Hindsight Memory] Initialized with capacity=%d", MAX_MEMORY)

    def record_scan(self, url: str, features, prediction: dict) -> dict:
        """Store a scan result in the memory core."""
        self._scan_count += 1
        record_id = str(uuid.uuid4())[:12]
        now = datetime.now(timezone.utc)

        domain = features.domain if hasattr(features, 'domain') else ""
        feature_vector = features_to_vector(features)

        record = {
            "id": record_id,
            "url": url,
            "domain": domain,
            "risk_score": prediction.get("probability", 0),
            "threat_level": prediction.get("threat_level", "low"),
            "confidence": prediction.get("confidence", 0.0),
            "scanned_at": now.isoformat(),
            "relative_time": "just now",
            "anomaly_count": len(features.anomalies) if hasattr(features, 'anomalies') else 0,
            "feature_vector": feature_vector,
        }

        self._records.appendleft(record)

        # Index by domain
        if domain:
            if domain not in self._domain_index:
                self._domain_index[domain] = []
            self._domain_index[domain].append(record_id)

        # Adaptive learning: if we've seen this domain before, adjust confidence
        domain_history = self._domain_index.get(domain, [])
        if len(domain_history) > 1:
            record["confidence"] = min(record["confidence"] + 2.0, 99.5)
            record["_revisit"] = True

        return record

    def get_history(self, limit: int = 20, threat_level: str = None) -> List[dict]:
        """Retrieve scan history with optional filtering."""
        self._refresh_relative_times()
        records = list(self._records)
        if threat_level:
            records = [r for r in records if r["threat_level"] == threat_level]
        return records[:limit]

    def get_record_by_id(self, record_id: str) -> Optional[dict]:
        for r in self._records:
            if r["id"] == record_id:
                return r
        return None

    def find_similar(self, feature_vector: List[float], limit: int = 10,
                     threshold: float = 0.5) -> List[dict]:
        """Find similar threats using cosine similarity on feature vectors."""
        from services.similarity_engine import cosine_similarity
        matches = []
        for record in self._records:
            rv = record.get("feature_vector")
            if not rv:
                continue
            sim = cosine_similarity(feature_vector, rv)
            if sim >= threshold:
                reasons = self._compute_match_reasons(sim, record)
                matches.append({
                    "url": record["url"],
                    "domain": record["domain"],
                    "similarity_score": round(sim, 4),
                    "match_reasons": reasons,
                    "threat_level": record["threat_level"],
                    "risk_score": record["risk_score"],
                    "scanned_at": record["scanned_at"],
                })
        matches.sort(key=lambda x: x["similarity_score"], reverse=True)
        return matches[:limit]

    def get_threat_timeline(self, domain: str = None) -> List[dict]:
        """Generate a threat evolution timeline for a domain or all threats."""
        self._refresh_relative_times()
        records = list(self._records)
        if domain:
            records = [r for r in records if r.get("domain") == domain]
        records.reverse()  # chronological order
        timeline = []
        for r in records:
            level = r.get("threat_level", "low")
            event = "Threat detected" if level in ("high", "critical") else \
                    "Suspicious activity" if level == "medium" else "URL scanned"
            timeline.append({
                "timestamp": r["scanned_at"],
                "event": event,
                "threat_level": level,
                "details": f"{r['url'][:60]} — risk {r['risk_score']}%",
            })
        return timeline

    def get_stats(self) -> Dict[str, Any]:
        """Aggregate statistics from the memory store."""
        total = len(self._records)
        if total == 0:
            return {"total_scans": self._scan_count, "stored_records": 0,
                    "high_risk": 0, "safe": 0, "average_risk": 0,
                    "top_domains": [], "threat_distribution": {}}

        high_risk = sum(1 for r in self._records if r["risk_score"] >= 55)
        safe = sum(1 for r in self._records if r["risk_score"] < 10)
        avg_risk = round(sum(r["risk_score"] for r in self._records) / total, 1)

        # Threat distribution
        dist = {}
        for r in self._records:
            lvl = r["threat_level"]
            dist[lvl] = dist.get(lvl, 0) + 1

        # Top targeted domains
        domain_counts = {}
        for r in self._records:
            d = r.get("domain", "unknown")
            domain_counts[d] = domain_counts.get(d, 0) + 1
        top_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "total_scans": self._scan_count,
            "stored_records": total,
            "high_risk": high_risk,
            "safe": safe,
            "average_risk": avg_risk,
            "threat_distribution": dist,
            "top_domains": [{"domain": d, "count": c} for d, c in top_domains],
            "memory_utilization": round(total / MAX_MEMORY * 100, 1),
        }

    def _compute_match_reasons(self, similarity: float, record: dict) -> List[str]:
        reasons = []
        if similarity > 0.9:
            reasons.append("Near-identical feature profile")
        elif similarity > 0.75:
            reasons.append("Highly similar structural patterns")
        else:
            reasons.append("Partial feature overlap")
        if record.get("threat_level") in ("high", "critical"):
            reasons.append(f"Previously flagged as {record['threat_level']} risk")
        return reasons

    def _refresh_relative_times(self):
        now = datetime.now(timezone.utc)
        for record in self._records:
            try:
                ts = datetime.fromisoformat(record["scanned_at"])
                delta = int((now - ts).total_seconds())
                if delta < 60: record["relative_time"] = "just now"
                elif delta < 3600: record["relative_time"] = f"{delta // 60} min ago"
                elif delta < 86400: record["relative_time"] = f"{delta // 3600} hr ago"
                else: record["relative_time"] = f"{delta // 86400} day(s) ago"
            except Exception:
                record["relative_time"] = "unknown"

    @property
    def uptime_seconds(self) -> float:
        return (datetime.now(timezone.utc) - self._started_at).total_seconds()


# ── Singleton Instance ────────────────────────────────────────────────────────
memory_store = ThreatMemoryStore()
