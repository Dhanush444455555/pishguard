"""
utils/feature_extractor.py — Feature vectorization for PhishGuard AI.
Converts UrlFeatures dataclass into numeric vectors for similarity computation
and provides feature normalization utilities.
"""

import math
from typing import List, Dict
from dataclasses import asdict


# ── Feature Vector Keys (ordered) ─────────────────────────────────────────────
# These define the canonical order of features in the vector.
VECTOR_KEYS = [
    "url_length",
    "domain_length",
    "digit_count",
    "hyphen_count",
    "dot_count",
    "subdomain_depth",
    "path_depth",
    "query_param_count",
    "has_ip",
    "has_at_symbol",
    "has_double_slash",
    "has_hex_encoding",
    "has_port",
    "has_https",
    "is_suspicious_tld",
    "is_safe_domain",
    "brand_in_subdomain",
    "brand_in_path",
    "brand_count",
    "domain_entropy",
    "path_entropy",
]

# ── Normalization ranges (min, max) for numeric features ──────────────────────
NORMALIZATION_RANGES = {
    "url_length": (0, 500),
    "domain_length": (0, 100),
    "digit_count": (0, 20),
    "hyphen_count": (0, 10),
    "dot_count": (0, 15),
    "subdomain_depth": (0, 8),
    "path_depth": (0, 10),
    "query_param_count": (0, 20),
    "brand_count": (0, 10),
    "domain_entropy": (0.0, 5.0),
    "path_entropy": (0.0, 5.0),
}


def features_to_vector(features) -> List[float]:
    """
    Convert a UrlFeatures dataclass into a normalized float vector.

    Args:
        features: UrlFeatures dataclass instance.

    Returns:
        List of floats (length = len(VECTOR_KEYS)) with values in [0, 1].
    """
    feature_dict = asdict(features) if hasattr(features, "__dataclass_fields__") else features
    vector = []

    for key in VECTOR_KEYS:
        raw = feature_dict.get(key, 0)

        # Boolean features → 0.0 or 1.0
        if isinstance(raw, bool):
            vector.append(1.0 if raw else 0.0)
        elif key in NORMALIZATION_RANGES:
            lo, hi = NORMALIZATION_RANGES[key]
            normalized = (float(raw) - lo) / (hi - lo) if hi > lo else 0.0
            vector.append(max(0.0, min(1.0, normalized)))
        else:
            vector.append(float(raw))

    return vector


def vector_magnitude(v: List[float]) -> float:
    """Compute the L2 norm (magnitude) of a vector."""
    return math.sqrt(sum(x * x for x in v))


def feature_importance_ranking(features, weights: Dict[str, float]) -> List[Dict]:
    """
    Rank features by their contribution to the phishing score.

    Args:
        features: UrlFeatures dataclass or dict.
        weights: Weight mapping {feature_name: weight_value}.

    Returns:
        Sorted list of dicts with feature name, weight, triggered status.
    """
    feature_dict = asdict(features) if hasattr(features, "__dataclass_fields__") else features
    ranking = []

    for key, weight in weights.items():
        value = feature_dict.get(key, False)
        triggered = bool(value) if isinstance(value, bool) else (value > 0 if isinstance(value, (int, float)) else False)
        ranking.append({
            "feature": key,
            "weight": weight,
            "triggered": triggered,
            "contribution": weight if triggered else 0.0,
        })

    ranking.sort(key=lambda x: abs(x["contribution"]), reverse=True)
    return ranking
