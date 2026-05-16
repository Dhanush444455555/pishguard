"""
services/similarity_engine.py — Threat similarity computation for PhishGuard AI.
Provides cosine similarity, Jaccard similarity, and Levenshtein distance
for threat matching and typosquat detection.
"""

import math
from typing import List, Set


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Compute cosine similarity between two feature vectors.
    Returns a value in [0, 1] where 1 = identical direction.
    """
    if len(vec_a) != len(vec_b) or not vec_a:
        return 0.0

    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))

    if mag_a == 0 or mag_b == 0:
        return 0.0

    return max(0.0, min(1.0, dot / (mag_a * mag_b)))


def jaccard_similarity(set_a: Set[str], set_b: Set[str]) -> float:
    """
    Compute Jaccard similarity between two sets of anomaly/feature labels.
    Returns a value in [0, 1] where 1 = identical sets.
    """
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0

    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Compute Levenshtein (edit) distance between two strings.
    Useful for detecting typosquatting domains.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    prev_row = list(range(len(s2) + 1))

    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row

    return prev_row[-1]


def domain_similarity(domain_a: str, domain_b: str) -> float:
    """
    Compute normalized similarity between two domains using Levenshtein distance.
    Returns a value in [0, 1] where 1 = identical.
    """
    if domain_a == domain_b:
        return 1.0
    if not domain_a or not domain_b:
        return 0.0

    max_len = max(len(domain_a), len(domain_b))
    distance = levenshtein_distance(domain_a.lower(), domain_b.lower())
    return 1.0 - (distance / max_len)


def is_typosquat(domain: str, target_brand: str, threshold: float = 0.85) -> bool:
    """
    Check if a domain is a potential typosquat of a target brand domain.
    Uses normalized Levenshtein distance.
    """
    # Strip TLD for comparison
    domain_base = domain.split(".")[0] if "." in domain else domain
    return domain_similarity(domain_base, target_brand) >= threshold


def compute_anomaly_overlap(anomalies_a: List[dict], anomalies_b: List[dict]) -> float:
    """
    Compute overlap between two anomaly lists using Jaccard similarity
    on anomaly titles.
    """
    set_a = {a.get("title", "") for a in anomalies_a}
    set_b = {a.get("title", "") for a in anomalies_b}
    return jaccard_similarity(set_a, set_b)
