"""
utils/url_parser.py — URL normalization and utility functions.
Provides safe canonicalization, defanging for logs, and domain extraction.
"""

import re
from urllib.parse import urlparse, urlunparse, unquote


def normalize_url(url: str) -> str:
    """
    Normalize a URL to a canonical form:
    - Ensure scheme is present (default to https)
    - Lowercase scheme and host
    - Remove default port (80/443)
    - Remove trailing slashes from path
    - Decode unnecessary percent-encoding
    """
    url = url.strip()

    if not re.match(r"^https?://", url, re.IGNORECASE):
        url = "https://" + url

    try:
        parsed = urlparse(url)
    except Exception:
        return url

    scheme = (parsed.scheme or "https").lower()
    host = (parsed.hostname or "").lower()
    port = parsed.port

    # Remove default ports
    if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
        port = None

    netloc = host
    if port:
        netloc = f"{host}:{port}"
    if parsed.username:
        user_info = parsed.username
        if parsed.password:
            user_info += f":{parsed.password}"
        netloc = f"{user_info}@{netloc}"

    path = parsed.path.rstrip("/") or "/"
    path = unquote(path)

    return urlunparse((scheme, netloc, path, parsed.params, parsed.query, ""))


def defang_url(url: str) -> str:
    """
    Defang a URL for safe display in logs and reports.
    Replaces 'http' -> 'hxxp', dots in domain -> '[.]'

    Example: https://evil.com -> hxxps://evil[.]com
    """
    defanged = url.replace("http://", "hxxp://").replace("https://", "hxxps://")

    try:
        parsed = urlparse(url)
        domain = parsed.hostname or ""
        if domain:
            defanged_domain = domain.replace(".", "[.]")
            defanged = defanged.replace(domain, defanged_domain, 1)
    except Exception:
        pass

    return defanged


def extract_apex_domain(url: str) -> str:
    """
    Extract the apex (registered) domain from a URL.
    e.g., 'https://login.secure.paypal.example.com/auth' -> 'example.com'
    """
    try:
        parsed = urlparse(url if "://" in url else f"https://{url}")
        host = parsed.hostname or ""
        parts = host.split(".")
        if len(parts) >= 2:
            return ".".join(parts[-2:])
        return host
    except Exception:
        return ""


def extract_all_subdomains(url: str) -> list:
    """
    Extract all subdomain levels from a URL.
    e.g., 'https://a.b.c.example.com' -> ['a', 'b', 'c']
    """
    try:
        parsed = urlparse(url if "://" in url else f"https://{url}")
        host = parsed.hostname or ""
        parts = host.split(".")
        if len(parts) > 2:
            return parts[:-2]
        return []
    except Exception:
        return []


def is_valid_url(url: str) -> bool:
    """Basic URL validity check."""
    url = url.strip()
    if not url:
        return False
    if not re.match(r"^https?://", url, re.IGNORECASE):
        url = "https://" + url
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False
