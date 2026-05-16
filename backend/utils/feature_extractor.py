"""
PhishGuard AI — URL Feature Extractor
======================================
Extracts structural & lexical features from URLs for phishing detection.
This module is used both during training (notebooks/model_training.py)
and at inference time (backend/services/ml_predictor.py).
"""

import re
import math
from urllib.parse import urlparse, parse_qs

# ─────────────────────────────────────────────────────────────────────
# Known URL shortener domains & suspicious TLDs / keywords
# ─────────────────────────────────────────────────────────────────────
SHORTENER_DOMAINS = {
    "bit.ly", "goo.gl", "tinyurl.com", "t.co", "ow.ly", "is.gd",
    "buff.ly", "adf.ly", "bit.do", "mcaf.ee", "su.pr", "db.tt",
    "qr.ae", "lnkd.in", "rb.gy", "cutt.ly", "shorturl.at", "v.gd",
    "rebrand.ly", "zpr.io",
}

SUSPICIOUS_TLDS = {
    ".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".pw",
    ".cc", ".buzz", ".club", ".work", ".icu", ".cam", ".surf",
    ".rest", ".monster", ".quest",
}

SUSPICIOUS_KEYWORDS = {
    "login", "signin", "verify", "account", "update", "secure",
    "banking", "confirm", "password", "credential", "suspend",
    "unlock", "alert", "notification", "paypal", "apple", "microsoft",
    "amazon", "netflix", "support", "helpdesk", "service", "webscr",
    "ebayisapi", "wp-login", "admin", "authenticate",
}


def shannon_entropy(s: str) -> float:
    """Calculate Shannon entropy of a string."""
    if not s:
        return 0.0
    prob = [s.count(c) / len(s) for c in set(s)]
    return -sum(p * math.log2(p) for p in prob if p > 0)


def has_ip_pattern(url: str) -> int:
    """Check if the URL contains an IP address instead of a domain name."""
    ip_pat = re.compile(
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)"
    )
    hex_ip = re.compile(r"0x[0-9a-fA-F]{1,2}(?:\.0x[0-9a-fA-F]{1,2}){3}")
    return int(bool(ip_pat.search(url) or hex_ip.search(url)))


def extract_features(url: str) -> dict:
    """
    Extract a rich set of structural / lexical features from a single URL.
    Returns a flat dictionary with 25 features.
    """
    raw_url = url
    if not url.startswith(("http://", "https://", "ftp://")):
        url = "http://" + url

    try:
        parsed = urlparse(url)
    except Exception:
        parsed = urlparse("http://invalid.example.com")

    domain = parsed.netloc.lower().split(":")[0]
    path = parsed.path or ""
    query = parsed.query or ""
    fragment = parsed.fragment or ""
    full = raw_url.lower()

    # Length features
    url_length = len(raw_url)
    domain_length = len(domain)
    path_length = len(path)

    # Count features
    num_dots = full.count(".")
    num_hyphens = full.count("-")
    num_underscores = full.count("_")
    num_slashes = full.count("/")
    num_digits = sum(c.isdigit() for c in full)
    num_params = len(parse_qs(query))
    num_fragments = 1 if fragment else 0
    num_special = sum(
        not c.isalnum() and c not in (".", "/", ":", "-", "_") for c in full
    )

    domain_parts = domain.split(".")
    num_subdomains = max(0, len(domain_parts) - 2)

    # Ratio features
    url_len_safe = max(url_length, 1)
    digit_ratio = num_digits / url_len_safe
    letter_ratio = sum(c.isalpha() for c in full) / url_len_safe
    special_char_ratio = num_special / url_len_safe

    # Boolean features
    has_ip = has_ip_pattern(raw_url)
    has_at = int("@" in raw_url)
    has_double_slash_redirect = int("//" in raw_url[8:]) if len(raw_url) > 8 else 0
    has_https = int(raw_url.lower().startswith("https"))
    is_shortened = int(domain in SHORTENER_DOMAINS)
    has_suspicious_tld = int(any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS))
    has_suspicious_keyword = int(any(kw in full for kw in SUSPICIOUS_KEYWORDS))

    # Entropy
    url_entropy = shannon_entropy(raw_url)

    # Domain token features
    domain_tokens = re.split(r"[.\-_]", domain)
    domain_token_count = len(domain_tokens)
    longest_domain_token = max((len(t) for t in domain_tokens), default=0)

    return {
        "url_length": url_length,
        "domain_length": domain_length,
        "path_length": path_length,
        "num_dots": num_dots,
        "num_hyphens": num_hyphens,
        "num_underscores": num_underscores,
        "num_slashes": num_slashes,
        "num_digits": num_digits,
        "num_params": num_params,
        "num_fragments": num_fragments,
        "num_subdomains": num_subdomains,
        "num_special_chars": num_special,
        "digit_ratio": digit_ratio,
        "letter_ratio": letter_ratio,
        "special_char_ratio": special_char_ratio,
        "has_ip_address": has_ip,
        "has_at_symbol": has_at,
        "has_double_slash_redirect": has_double_slash_redirect,
        "has_https": has_https,
        "is_shortened": is_shortened,
        "has_suspicious_tld": has_suspicious_tld,
        "has_suspicious_keyword": has_suspicious_keyword,
        "url_entropy": url_entropy,
        "domain_token_count": domain_token_count,
        "longest_domain_token_len": longest_domain_token,
    }


# Canonical feature name order (must match training)
FEATURE_NAMES = list(extract_features("http://example.com").keys())
