"""
ai/reasoning.py — Threat Reasoning Engine for PhishGuard AI.
Generates human-readable AI analysis using chain-of-thought reasoning
from feature data and memory context. Fully local — no external API calls.
"""

from typing import List, Dict, Any
from ai.prompts import (
    get_summary_template, get_recommendations,
    get_category_narrative, REASONING_STEPS,
)
from services.url_analyzer import BRAND_KEYWORDS


class ThreatReasoningEngine:
    """
    Generates structured threat narratives using deterministic
    chain-of-thought reasoning from extracted features and ML scores.
    """

    def reason(self, features, prediction: dict, similar_threats: list = None) -> dict:
        """
        Perform full reasoning over a URL analysis.

        Returns:
            dict with: summary, reasoning_chain, categories, recommendations
        """
        threat_level = prediction.get("threat_level", "medium")
        risk_score = prediction.get("probability", 0)
        confidence = prediction.get("confidence", 0)
        zero_day = prediction.get("zero_day_probability", 0.0)

        # ── Build reasoning chain ─────────────────────────────────────────
        chain = self._build_reasoning_chain(features, prediction, similar_threats or [])

        # ── Identify threat categories ────────────────────────────────────
        categories = self._identify_categories(features)

        # ── Generate summary narrative ────────────────────────────────────
        detail = self._build_detail_string(features, categories, risk_score)
        template = get_summary_template(threat_level)
        summary = template.format(detail=detail)

        # ── Get recommendations ───────────────────────────────────────────
        recs = get_recommendations(threat_level)

        # ── Confidence explanation ────────────────────────────────────────
        conf_explanation = self._explain_confidence(
            confidence, len(features.anomalies), len(similar_threats or [])
        )

        return {
            "summary": summary,
            "reasoning_chain": chain,
            "categories": categories,
            "recommendations": recs,
            "confidence_explanation": conf_explanation,
        }

    def _build_reasoning_chain(self, features, prediction, similar_threats) -> List[str]:
        chain = []

        # Step 1: Feature extraction
        chain.append(REASONING_STEPS["feature_extraction"].format(
            feature_count=21 + len(features.suspicious_keywords)
        ))

        # Step 2: Entropy
        chain.append(REASONING_STEPS["entropy_analysis"].format(
            d_entropy=features.domain_entropy, p_entropy=features.path_entropy
        ))

        # Step 3: Brand check
        chain.append(REASONING_STEPS["brand_check"].format(
            brand_db_size=len(BRAND_KEYWORDS),
            match_count=features.brand_count
        ))

        # Step 4: TLD
        chain.append(REASONING_STEPS["tld_analysis"].format(
            tld=features.tld,
            classification="suspicious" if features.is_suspicious_tld else "standard"
        ))

        # Step 5: IDN
        chain.append(REASONING_STEPS["idn_check"].format(
            homoglyph_count=features.homoglyph_count
        ))

        # Step 6: Keywords
        kw_categories = set(k["category"] for k in features.suspicious_keywords)
        chain.append(REASONING_STEPS["keyword_scan"].format(
            kw_count=len(features.suspicious_keywords),
            categories=len(kw_categories)
        ))

        # Step 7: Redirect
        chain.append(REASONING_STEPS["redirect_analysis"].format(
            redirect_count=len(features.redirect_chain)
        ))

        # Step 8: ML scoring
        chain.append(REASONING_STEPS["ml_scoring"].format(
            score=prediction.get("probability", 0),
            confidence=prediction.get("confidence", 0)
        ))

        # Step 9: Memory lookup
        chain.append(REASONING_STEPS["memory_lookup"].format(
            similar_count=len(similar_threats)
        ))

        # Step 10: Zero-day
        chain.append(REASONING_STEPS["zero_day_check"].format(
            zero_day=prediction.get("zero_day_probability", 0)
        ))

        return chain

    def _identify_categories(self, features) -> List[str]:
        categories = []
        if features.brand_in_subdomain and not features.is_safe_domain:
            categories.append("brand_impersonation")
        cred = [k for k in features.suspicious_keywords if k["category"] == "credential"]
        if cred and not features.is_safe_domain:
            categories.append("credential_harvesting")
        if features.has_punycode or features.homoglyph_count > 0:
            categories.append("domain_spoofing")
        if features.has_hex_encoding or features.has_double_slash or features.redirect_chain:
            categories.append("obfuscation")
        if features.domain_entropy > 4.0 and not features.is_safe_domain:
            categories.append("dga_suspected")
        if features.is_safe_domain and not features.anomalies:
            categories.append("safe_domain")
        if not categories and features.anomalies:
            categories.append("structural_anomaly")
        return categories

    def _build_detail_string(self, features, categories: List[str], risk_score: int) -> str:
        parts = []
        if "brand_impersonation" in categories:
            brands = [b for b in BRAND_KEYWORDS if b in features.raw_url.lower()]
            if brands:
                parts.append(f"Impersonates '{brands[0]}'")
        if "credential_harvesting" in categories:
            parts.append("Contains credential harvesting keywords")
        if "domain_spoofing" in categories:
            parts.append("Uses domain spoofing techniques")
        if "obfuscation" in categories:
            parts.append("Employs URL obfuscation")
        anomaly_count = len(features.anomalies)
        if anomaly_count:
            parts.append(f"{anomaly_count} anomalies detected")
        parts.append(f"Risk score: {risk_score}/100")
        return ". ".join(parts) + "." if parts else ""

    def _explain_confidence(self, confidence: float, anomaly_count: int,
                            similar_count: int) -> str:
        parts = [f"Confidence score of {confidence}% is derived from:"]
        parts.append(f"  • Base engine confidence: 87%")
        parts.append(f"  • {anomaly_count} detected anomalies (+{anomaly_count * 1.5:.1f}%)")
        if similar_count:
            parts.append(f"  • {similar_count} matching historical threats (corroborating evidence)")
        if confidence > 95:
            parts.append("  → Very high confidence — multiple independent signals converge")
        elif confidence > 90:
            parts.append("  → High confidence — strong signal agreement")
        else:
            parts.append("  → Moderate confidence — limited confirming signals")
        return "\n".join(parts)


# ── Singleton ─────────────────────────────────────────────────────────────────
reasoning_engine = ThreatReasoningEngine()
