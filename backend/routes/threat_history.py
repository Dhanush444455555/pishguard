"""
routes/threat_history.py — GET /api/v1/threat-history & GET /api/v1/similar-threats
Exposes the Hindsight Memory data for threat history and similarity search.
"""

from fastapi import APIRouter, Query, HTTPException

from services.sentinel_memory import memory_store
from services.url_analyzer import extract_features
from utils.feature_extractor import features_to_vector
from utils.url_parser import is_valid_url

router = APIRouter()


@router.get("/threat-history", summary="Retrieve threat scan history",
            description="Paginated scan history from the Hindsight Memory")
async def threat_history(
    limit: int = Query(default=20, ge=1, le=100, description="Max records"),
    threat_level: str = Query(default=None, description="Filter by threat level"),
):
    """
    Returns recent scan history with optional filtering by threat level.
    """
    records = memory_store.get_history(limit=limit, threat_level=threat_level)
    stats = memory_store.get_stats()

    # Strip feature vectors from response (internal data)
    clean_records = []
    for r in records:
        rec = {k: v for k, v in r.items() if k != "feature_vector" and k != "_revisit"}
        clean_records.append(rec)

    return {
        "total_records": len(clean_records),
        "records": clean_records,
        "stats": stats,
    }


@router.get("/similar-threats", summary="Find similar threats",
            description="Query Hindsight Memory for threats similar to a given URL")
async def similar_threats(
    url: str = Query(..., min_length=3, description="URL to find similar threats for"),
    limit: int = Query(default=10, ge=1, le=50, description="Max results"),
    threshold: float = Query(default=0.5, ge=0.0, le=1.0, description="Min similarity"),
):
    """
    Extracts features from the query URL and searches the memory core
    for previously scanned URLs with similar feature profiles.
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    if not is_valid_url(url):
        raise HTTPException(status_code=422, detail=f"Invalid URL: {url}")

    features = extract_features(url)
    fv = features_to_vector(features)
    matches = memory_store.find_similar(fv, limit=limit, threshold=threshold)

    return {
        "query_url": url,
        "total_matches": len(matches),
        "matches": matches,
    }
