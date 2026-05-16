"""
services/url_analyzer.py — Advanced URL feature extraction for PhishGuard AI.
Extracts comprehensive features including structural analysis, brand impersonation,
homoglyph/punycode detection, keyword analysis, and redirect chain detection.
"""

import re
import math
from urllib.parse import urlparse, parse_qs
from dataclasses import dataclass, field
from typing import List, Dict

# ── Threat Intelligence Dictionaries ──────────────────────────────────────────

BRAND_KEYWORDS = [
    "paypal", "apple", "microsoft", "google", "amazon", "facebook", "netflix",
    "instagram", "twitter", "linkedin", "dropbox", "office365", "icloud",
    "outlook", "gmail", "yahoo", "chase", "wellsfargo", "bankofamerica",
    "citibank", "hsbc", "ebay", "walmart", "coinbase", "binance", "metamask",
    "stripe", "shopify", "docusign", "adobe", "zoom", "teams", "slack",
]

CREDENTIAL_KEYWORDS = [
    "login", "signin", "sign-in", "authenticate", "password", "credential",
    "verify", "validate", "confirm", "account", "secure", "auth", "sso", "token",
]

URGENCY_KEYWORDS = [
    "alert", "warning", "suspend", "unusual", "expire", "urgent", "immediate",
    "locked", "blocked", "unauthorized", "compromised", "frozen", "deactivate",
]

FINANCIAL_KEYWORDS = [
    "payment", "invoice", "billing", "refund", "transfer", "bank", "credit",
    "transaction", "wallet", "withdraw", "deposit", "claim", "reward", "prize",
]

SUSPICIOUS_TLDS = {
    ".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".club", ".info",
    ".biz", ".icu", ".vip", ".shop", ".online", ".site", ".live", ".click",
    ".buzz", ".work", ".download", ".zip", ".review", ".date", ".faith",
    ".stream", ".gdn", ".loan", ".win", ".racing", ".party", ".trade",
}

SAFE_DOMAINS = {
    "google.com", "youtube.com", "facebook.com", "twitter.com", "wikipedia.org",
    "amazon.com", "reddit.com", "linkedin.com", "github.com", "microsoft.com",
    "apple.com", "instagram.com", "netflix.com", "stackoverflow.com",
    "medium.com", "paypal.com", "ebay.com", "dropbox.com", "zoom.us",
}

HOMOGLYPHS = {
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y",
    "х": "x", "ѕ": "s", "і": "i", "ј": "j", "0": "o", "1": "l",
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _entropy(s: str) -> float:
    if not s:
        return 0.0
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    n = len(s)
    return -sum((f / n) * math.log2(f / n) for f in freq.values())


def _detect_homoglyphs(domain: str) -> List[Dict]:
    return [{"position": i, "character": c, "looks_like": HOMOGLYPHS[c]}
            for i, c in enumerate(domain) if c in HOMOGLYPHS]


def _detect_punycode(domain: str) -> bool:
    return any(p.startswith("xn--") for p in domain.split("."))


def _analyze_keywords(url_lower, path_lower, subdomain_lower) -> List[Dict]:
    results = []
    for category, keywords, severity in [
        ("credential", CREDENTIAL_KEYWORDS, "high"),
        ("urgency", URGENCY_KEYWORDS, "high"),
        ("brand", BRAND_KEYWORDS, "medium"),
        ("financial", FINANCIAL_KEYWORDS, "high"),
    ]:
        for kw in keywords:
            locs = []
            if kw in subdomain_lower: locs.append("subdomain")
            if kw in path_lower: locs.append("path")
            if locs:
                results.append({"keyword": kw, "category": category,
                                "severity": severity, "context": ", ".join(locs)})
    return results


def _detect_redirect_patterns(url: str, path: str) -> List[Dict]:
    chain = []
    patterns = [("/redirect", "Explicit redirect"), ("/goto", "Goto redirect"),
                ("/click", "Click tracking"), ("url=", "URL parameter redirect"),
                ("next=", "Next-page redirect"), ("dest=", "Destination param")]
    for pat, desc in patterns:
        if pat.lower() in url.lower():
            chain.append({"url": url[:80], "status_hint": "redirect_pattern",
                          "suspicious": True, "description": desc})
    if url.count("%25") > 0:
        chain.append({"url": url[:80], "status_hint": "double_encoding",
                      "suspicious": True, "description": "Double URL encoding detected"})
    if re.search(r"https?://", path[1:]) if len(path) > 1 else False:
        chain.append({"url": url[:80], "status_hint": "embedded_url",
                      "suspicious": True, "description": "URL embedded within path"})
    return chain


# ── Feature Dataclass ─────────────────────────────────────────────────────────

@dataclass
class UrlFeatures:
    raw_url: str
    scheme: str = ""
    domain: str = ""
    subdomain: str = ""
    tld: str = ""
    path: str = ""
    url_length: int = 0
    domain_length: int = 0
    digit_count: int = 0
    hyphen_count: int = 0
    dot_count: int = 0
    subdomain_depth: int = 0
    path_depth: int = 0
    query_param_count: int = 0
    has_ip: bool = False
    has_at_symbol: bool = False
    has_double_slash: bool = False
    has_hex_encoding: bool = False
    has_port: bool = False
    has_https: bool = False
    is_suspicious_tld: bool = False
    is_safe_domain: bool = False
    brand_in_subdomain: bool = False
    brand_in_path: bool = False
    brand_count: int = 0
    has_punycode: bool = False
    homoglyph_count: int = 0
    homoglyphs_detected: List[Dict] = field(default_factory=list)
    domain_entropy: float = 0.0
    path_entropy: float = 0.0
    suspicious_keywords: List[Dict] = field(default_factory=list)
    redirect_chain: List[Dict] = field(default_factory=list)
    anomalies: List[Dict] = field(default_factory=list)


# ── Main Extractor ────────────────────────────────────────────────────────────

def extract_features(url: str) -> UrlFeatures:
    f = UrlFeatures(raw_url=url)
    url_to_parse = url if re.match(r"^https?://", url, re.I) else "http://" + url

    try:
        parsed = urlparse(url_to_parse)
    except Exception:
        return f

    f.scheme = parsed.scheme or ""
    f.has_https = f.scheme == "https"
    f.path = parsed.path or ""
    f.domain = parsed.hostname or ""
    f.has_port = parsed.port is not None

    parts = f.domain.split(".")
    if len(parts) >= 2:
        f.tld = "." + parts[-1]
        f.subdomain = ".".join(parts[:-2]) if len(parts) > 2 else ""
    else:
        f.tld = f.domain

    apex = ".".join(parts[-2:]) if len(parts) >= 2 else f.domain
    f.is_safe_domain = apex in SAFE_DOMAINS
    f.url_length = len(url)
    f.domain_length = len(f.domain)
    f.digit_count = sum(c.isdigit() for c in f.domain)
    f.hyphen_count = f.domain.count("-")
    f.dot_count = url.count(".")
    f.subdomain_depth = len(f.subdomain.split(".")) if f.subdomain else 0
    f.path_depth = len([p for p in f.path.split("/") if p])
    f.query_param_count = len(parse_qs(parsed.query))
    f.has_ip = bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", f.domain))
    f.has_at_symbol = "@" in url
    f.has_double_slash = "//" in (parsed.path or "")
    f.has_hex_encoding = "%" in url
    f.is_suspicious_tld = f.tld in SUSPICIOUS_TLDS

    url_lower = url.lower()
    path_lower = f.path.lower()
    subdomain_lower = f.subdomain.lower()
    matched_brands = [b for b in BRAND_KEYWORDS if b in url_lower]
    f.brand_count = len(matched_brands)
    f.brand_in_subdomain = any(b in subdomain_lower for b in BRAND_KEYWORDS)
    f.brand_in_path = any(b in path_lower for b in BRAND_KEYWORDS)

    f.has_punycode = _detect_punycode(f.domain)
    f.homoglyphs_detected = _detect_homoglyphs(f.domain)
    f.homoglyph_count = len(f.homoglyphs_detected)
    f.domain_entropy = _entropy(f.domain)
    f.path_entropy = _entropy(f.path)
    f.suspicious_keywords = _analyze_keywords(url_lower, path_lower, subdomain_lower)
    f.redirect_chain = _detect_redirect_patterns(url, f.path)

    # ── Anomaly Collection ────────────────────────────────────────────────
    _collect_anomalies(f)
    return f


def _collect_anomalies(f: UrlFeatures):
    """Populate anomalies list based on extracted features."""
    checks = [
        (f.has_ip, "IP Address as Host", "URL uses a raw IP address instead of a domain.", "critical", "structural"),
        (f.url_length > 100, "Abnormally Long URL", f"URL length ({f.url_length} chars) is unusually long.", "medium", "structural"),
        (f.has_at_symbol, "@ Symbol in URL", "The '@' tricks browsers into ignoring the visible domain.", "high", "obfuscation"),
        (f.hyphen_count >= 3, "Excessive Hyphens", f"Domain has {f.hyphen_count} hyphens — brand-spoofing indicator.", "medium", "structural"),
        (f.is_suspicious_tld, f"Suspicious TLD ({f.tld})", f"'{f.tld}' is frequently abused for phishing.", "high", "structural"),
        (f.has_double_slash, "Double Slash in Path", "Suggests redirect obfuscation.", "medium", "obfuscation"),
        (f.has_hex_encoding, "Hex Encoding Detected", "Percent-encoding used to bypass URL filters.", "high", "obfuscation"),
        (f.brand_in_subdomain and not f.is_safe_domain, "Brand Impersonation", "Brand keyword in subdomain of non-official domain.", "critical", "brand"),
        (not f.has_https, "No HTTPS", "Credentials over this URL are unencrypted.", "high", "protocol"),
        (f.subdomain_depth >= 3, "Deep Subdomain Structure", f"{f.subdomain_depth} levels — mimics legitimate URLs.", "medium", "structural"),
        (f.digit_count >= 4, "High Digit Count", f"Domain has {f.digit_count} digits — DGA indicator.", "low", "structural"),
        (f.has_port, "Non-standard Port", "May indicate a rogue server.", "medium", "structural"),
        (f.has_punycode, "Punycode/IDN Domain", "Internationalized encoding for visual spoofing.", "high", "obfuscation"),
        (f.homoglyph_count > 0, f"Homoglyph Characters ({f.homoglyph_count})", "Visually similar Unicode characters detected.", "critical", "obfuscation"),
        (f.domain_entropy > 4.0 and not f.is_safe_domain, "High Domain Entropy", f"Entropy {f.domain_entropy:.2f} bits — possible DGA.", "medium", "structural"),
        (len(f.redirect_chain) > 0, f"Redirect Patterns ({len(f.redirect_chain)})", "URL contains redirect chain indicators.", "high", "obfuscation"),
    ]

    cred_kw = [k for k in f.suspicious_keywords if k["category"] == "credential"]
    if cred_kw and not f.is_safe_domain:
        checks.append((True, f"Credential Keywords ({len(cred_kw)})", "Credential harvesting language detected.", "high", "brand"))

    urg_kw = [k for k in f.suspicious_keywords if k["category"] == "urgency"]
    if urg_kw and not f.is_safe_domain:
        checks.append((True, f"Urgency Keywords ({len(urg_kw)})", "Fear/urgency language detected.", "medium", "brand"))

    for condition, title, desc, impact, category in checks:
        if condition:
            f.anomalies.append({"title": title, "description": desc, "impact": impact, "category": category})
