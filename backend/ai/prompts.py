"""
ai/prompts.py — Threat narrative templates for PhishGuard AI.
Provides template library for generating human-readable threat analysis
narratives calibrated by severity and threat category.
"""

from typing import List, Dict


# ── Severity-Calibrated Summary Templates ─────────────────────────────────────

SUMMARY_TEMPLATES = {
    "critical": (
        "⛔ CRITICAL THREAT DETECTED — This URL exhibits multiple high-confidence "
        "indicators of a sophisticated phishing attack. {detail} "
        "Immediate blocking is strongly recommended."
    ),
    "high": (
        "🔴 HIGH RISK — This URL displays significant phishing characteristics. "
        "{detail} Exercise extreme caution — do not enter any credentials."
    ),
    "medium": (
        "🟡 MODERATE RISK — This URL shows some suspicious patterns that warrant "
        "investigation. {detail} Proceed with caution."
    ),
    "low": (
        "🟢 LOW RISK — This URL shows minimal suspicious indicators. {detail} "
        "Standard browsing precautions are sufficient."
    ),
    "safe": (
        "✅ SAFE — This URL belongs to a known legitimate domain with no detected "
        "anomalies. {detail}"
    ),
}


# ── Category-Specific Narratives ──────────────────────────────────────────────

CATEGORY_NARRATIVES = {
    "brand_impersonation": (
        "The URL impersonates a well-known brand by embedding brand keywords in "
        "non-official domain components. This is a hallmark of credential "
        "harvesting campaigns targeting {brand} users."
    ),
    "credential_harvesting": (
        "Multiple credential-related keywords (login, password, verify) are present "
        "in the URL structure, strongly suggesting this page is designed to capture "
        "user authentication data."
    ),
    "domain_spoofing": (
        "The domain uses techniques such as homoglyph characters, punycode encoding, "
        "or deep subdomains to visually mimic a legitimate website. This is a "
        "sophisticated attack vector."
    ),
    "obfuscation": (
        "The URL employs obfuscation techniques including hex encoding, redirect "
        "chains, or embedded URLs to evade automated detection systems and confuse "
        "users about the true destination."
    ),
    "structural_anomaly": (
        "Structural analysis reveals unusual URL characteristics including "
        "{anomaly_details}. These patterns are statistically correlated with "
        "phishing infrastructure."
    ),
    "dga_suspected": (
        "The domain exhibits high entropy ({entropy:.2f} bits), suggesting it may "
        "be algorithmically generated (Domain Generation Algorithm). DGA domains "
        "are commonly used in malware command-and-control infrastructure."
    ),
    "safe_domain": (
        "This URL resolves to a known, verified domain ({domain}). No structural "
        "anomalies, brand impersonation, or obfuscation techniques were detected."
    ),
}


# ── Reasoning Chain Templates ─────────────────────────────────────────────────

REASONING_STEPS = {
    "feature_extraction": "Extracted {feature_count} structural features from URL",
    "entropy_analysis": "Computed Shannon entropy: domain={d_entropy:.2f}, path={p_entropy:.2f}",
    "brand_check": "Scanned against {brand_db_size} known brand keywords — {match_count} matches found",
    "tld_analysis": "TLD '{tld}' classified as {classification}",
    "idn_check": "IDN/homoglyph scan: {homoglyph_count} suspicious characters detected",
    "keyword_scan": "Keyword analysis: {kw_count} suspicious keywords across {categories} categories",
    "redirect_analysis": "Redirect chain analysis: {redirect_count} redirect patterns identified",
    "ml_scoring": "Ensemble model scored URL at {score}/100 (confidence: {confidence}%)",
    "memory_lookup": "Hindsight Memory queried — {similar_count} similar threats found",
    "zero_day_check": "Zero-day probability estimated at {zero_day:.0%}",
}


# ── Recommendation Templates ─────────────────────────────────────────────────

RECOMMENDATIONS = {
    "critical": [
        "Block this URL immediately across all network endpoints",
        "Add the domain to your organization's threat blocklist",
        "Alert security operations center (SOC) for investigation",
        "Check if any users have already visited this URL",
        "Submit to threat intelligence sharing platforms (e.g., PhishTank, VirusTotal)",
    ],
    "high": [
        "Block this URL in web proxies and email filters",
        "Add the domain to the watchlist for continued monitoring",
        "Warn users who may have received this URL via email or messaging",
        "Investigate the domain's registration details and hosting provider",
    ],
    "medium": [
        "Add this URL to the monitoring watchlist",
        "Investigate further before allowing access",
        "Consider blocking at the DNS level as a precaution",
        "Review URL with your security team",
    ],
    "low": [
        "No immediate action required",
        "Continue standard monitoring protocols",
        "Re-scan periodically to check for changes",
    ],
    "safe": [
        "No action required — URL is from a verified domain",
    ],
}


def get_summary_template(threat_level: str) -> str:
    return SUMMARY_TEMPLATES.get(threat_level, SUMMARY_TEMPLATES["medium"])


def get_recommendations(threat_level: str) -> List[str]:
    return RECOMMENDATIONS.get(threat_level, RECOMMENDATIONS["medium"])


def get_category_narrative(category: str, **kwargs) -> str:
    template = CATEGORY_NARRATIVES.get(category, "")
    try:
        return template.format(**kwargs)
    except (KeyError, IndexError):
        return template
