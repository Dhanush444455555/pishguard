"""
services/threat_explainer.py — Explainable AI Engine for PhishGuard AI.
Generates structured explainability reports with feature contributions,
risk factor decomposition, and actionable recommendations.
"""

from typing import List, Dict
from ai.prompts import get_recommendations


class ExplainableAIEngine:
    """Generates structured reports that explain why a URL was flagged."""

    def explain(self, features, prediction: dict, reasoning: dict,
                similar_threats: list = None) -> dict:
        threat_level = prediction.get("threat_level", "medium")
        risk_score = prediction.get("probability", 0)
        breakdown = prediction.get("score_breakdown", [])
        zero_day = prediction.get("zero_day_probability", 0.0)

        # Risk factors from anomalies
        risk_factors = self._build_risk_factors(features)

        # Score contribution breakdown
        score_breakdown = self._format_score_breakdown(breakdown)

        # Keyword analysis
        keyword_analysis = self._format_keywords(features)

        # Redirect chain
        redirect_chain = self._format_redirects(features)

        # Zero-day assessment
        zero_day_assessment = self._build_zero_day(features, zero_day, risk_score)

        return {
            "summary": reasoning.get("summary", ""),
            "reasoning_chain": reasoning.get("reasoning_chain", []),
            "risk_factors": risk_factors,
            "score_breakdown": score_breakdown,
            "zero_day_assessment": zero_day_assessment,
            "keyword_analysis": keyword_analysis,
            "redirect_chain": redirect_chain,
            "recommendations": reasoning.get("recommendations", get_recommendations(threat_level)),
            "confidence_explanation": reasoning.get("confidence_explanation", ""),
        }

    def _build_risk_factors(self, features) -> List[dict]:
        factors = []
        for anomaly in features.anomalies:
            factors.append({
                "indicator_type": anomaly.get("category", "general"),
                "description": anomaly.get("title", ""),
                "severity": anomaly.get("impact", "medium"),
                "evidence": anomaly.get("description", ""),
            })
        return factors

    def _format_score_breakdown(self, breakdown: list) -> List[dict]:
        formatted = []
        for item in breakdown:
            formatted.append({
                "feature": item.get("feature", ""),
                "weight": item.get("weight", 0),
                "triggered": item.get("triggered", False),
                "description": item.get("description", ""),
            })
        return formatted

    def _format_keywords(self, features) -> List[dict]:
        return [
            {
                "keyword": kw.get("keyword", ""),
                "category": kw.get("category", ""),
                "severity": kw.get("severity", "medium"),
                "context": kw.get("context", ""),
            }
            for kw in features.suspicious_keywords
        ]

    def _format_redirects(self, features) -> List[dict]:
        return [
            {
                "url": r.get("url", ""),
                "status_hint": r.get("status_hint", ""),
                "suspicious": r.get("suspicious", False),
            }
            for r in features.redirect_chain
        ]

    def _build_zero_day(self, features, probability: float, risk_score: int) -> dict:
        novel = []
        if features.homoglyph_count > 0:
            novel.append("Homoglyph characters in domain")
        if features.has_punycode:
            novel.append("Punycode/IDN encoding")
        if features.domain_entropy > 4.2:
            novel.append(f"Very high domain entropy ({features.domain_entropy:.2f})")
        if len(features.redirect_chain) >= 2:
            novel.append("Multi-layer redirect chain")
        if risk_score >= 50 and not features.is_suspicious_tld:
            novel.append("High risk with non-flagged TLD (novel vector)")

        if probability >= 0.5:
            reasoning = (
                "This URL shows characteristics not commonly seen in known phishing "
                "databases, suggesting a potentially novel attack vector."
            )
            recommendation = "Escalate to threat research team for deep analysis"
        elif probability >= 0.2:
            reasoning = (
                "Some novel indicators present but insufficient evidence for "
                "zero-day classification."
            )
            recommendation = "Add to monitoring watchlist for pattern tracking"
        else:
            reasoning = "URL matches known threat patterns — low zero-day probability."
            recommendation = "Standard response protocols sufficient"

        return {
            "probability": probability,
            "reasoning": reasoning,
            "novel_indicators": novel,
            "recommendation": recommendation,
        }


explainer_engine = ExplainableAIEngine()
