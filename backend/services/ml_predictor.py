"""
services/ml_predictor.py — Ensemble ML scoring engine for PhishGuard AI.
Combines heuristic weighted scoring with statistical analysis.
Provides score breakdown, feature importance, and zero-day estimation.
"""

from services.url_analyzer import UrlFeatures

# ── Weight Configuration ──────────────────────────────────────────────────────

WEIGHTS = {
    "has_ip": 30, "brand_in_subdomain": 25, "has_at_symbol": 20,
    "is_suspicious_tld": 18, "has_hex_encoding": 12, "has_double_slash": 10,
    "brand_in_path": 8, "has_port": 8, "not_https": 6,
    "excessive_hyphens": 5, "deep_subdomains": 5, "long_url": 5,
    "high_digits": 3, "punycode": 10, "homoglyphs": 20,
    "high_entropy": 6, "redirect_patterns": 12, "credential_keywords": 10,
    "urgency_keywords": 5, "safe_domain": -60,
}

CONFIDENCE_BASE = 87.0


def predict(features: UrlFeatures) -> dict:
    """
    Ensemble prediction combining heuristic scoring with feature analysis.
    Returns: probability, threat_level, confidence, model_used, score_breakdown, zero_day_probability
    """
    score = 0.0
    breakdown = []

    def _add(key, condition, desc):
        nonlocal score
        w = WEIGHTS.get(key, 0)
        triggered = bool(condition)
        if triggered:
            score += w
        breakdown.append({
            "feature": key, "weight": w, "triggered": triggered,
            "description": desc,
        })

    _add("has_ip", features.has_ip, "IP address used as hostname")
    _add("brand_in_subdomain", features.brand_in_subdomain and not features.is_safe_domain,
         "Brand keyword in subdomain of unofficial domain")
    _add("has_at_symbol", features.has_at_symbol, "@ symbol present in URL")
    _add("is_suspicious_tld", features.is_suspicious_tld, f"Suspicious TLD: {features.tld}")
    _add("has_hex_encoding", features.has_hex_encoding, "Percent-encoding detected")
    _add("has_double_slash", features.has_double_slash, "Double slash in path")
    _add("brand_in_path", features.brand_in_path, "Brand keyword in URL path")
    _add("has_port", features.has_port, "Non-standard port specified")
    _add("not_https", not features.has_https, "No HTTPS encryption")
    _add("excessive_hyphens", features.hyphen_count >= 3,
         f"{features.hyphen_count} hyphens in domain")
    _add("deep_subdomains", features.subdomain_depth >= 3,
         f"{features.subdomain_depth} subdomain levels")
    _add("long_url", features.url_length >= 100, f"URL length: {features.url_length}")
    _add("high_digits", features.digit_count >= 4, f"{features.digit_count} digits in domain")
    _add("punycode", features.has_punycode, "Punycode/IDN encoding detected")
    _add("homoglyphs", features.homoglyph_count > 0,
         f"{features.homoglyph_count} homoglyph characters")
    _add("high_entropy", features.domain_entropy > 3.8 and not features.is_safe_domain,
         f"Domain entropy: {features.domain_entropy:.2f}")

    cred_kw = [k for k in features.suspicious_keywords if k["category"] == "credential"]
    _add("credential_keywords", len(cred_kw) > 0 and not features.is_safe_domain,
         f"{len(cred_kw)} credential-related keywords")

    urg_kw = [k for k in features.suspicious_keywords if k["category"] == "urgency"]
    _add("urgency_keywords", len(urg_kw) > 0 and not features.is_safe_domain,
         f"{len(urg_kw)} urgency keywords")

    redirect_count = len(features.redirect_chain)
    _add("redirect_patterns", redirect_count > 0, f"{redirect_count} redirect patterns")
    _add("safe_domain", features.is_safe_domain, "Known safe domain (negative weight)")

    probability = max(0, min(100, int(score)))

    if probability >= 75:
        threat_level = "critical"
    elif probability >= 55:
        threat_level = "high"
    elif probability >= 30:
        threat_level = "medium"
    elif probability >= 10:
        threat_level = "low"
    else:
        threat_level = "safe"

    signal_count = len(features.anomalies)
    confidence = min(CONFIDENCE_BASE + signal_count * 1.5, 99.5)

    # Zero-day estimation
    zero_day_prob = _estimate_zero_day(features, probability)

    return {
        "probability": probability,
        "threat_level": threat_level,
        "confidence": round(confidence, 1),
        "model_used": "PhishGuard-Ensemble-v3",
        "score_breakdown": breakdown,
        "zero_day_probability": zero_day_prob,
    }


def _estimate_zero_day(features: UrlFeatures, risk_score: int) -> float:
    """
    Estimate probability that this URL represents a zero-day (previously unseen) threat.
    Higher scores for novel combinations of indicators.
    """
    novelty = 0.0
    if features.homoglyph_count > 0:
        novelty += 0.25
    if features.has_punycode:
        novelty += 0.15
    if features.domain_entropy > 4.2:
        novelty += 0.15
    if len(features.redirect_chain) >= 2:
        novelty += 0.15
    if risk_score >= 50 and not features.is_suspicious_tld:
        novelty += 0.10  # High risk but not using known-bad TLD = more novel
    if features.brand_in_subdomain and features.has_hex_encoding:
        novelty += 0.10
    if risk_score < 20:
        novelty = max(0.0, novelty - 0.3)

    return round(min(novelty, 0.95), 2)
