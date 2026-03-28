from math import radians, cos, sin, asin, sqrt
from app.models.schemas import ResolutionResult, LandmarkCandidate
from app.services.dataset_service import get_landmarks


def haversine(lat1, lon1, lat2, lon2):
    if None in [lat1, lon1, lat2, lon2]:
        return float("inf")
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return 6371 * c


def detect_landmark(image_base64: str, lat: float | None, lng: float | None) -> ResolutionResult:
    landmarks = get_landmarks()

    ranked = []
    for lm in landmarks:
        d = haversine(lat, lng, lm["lat"], lm["lng"])
        ranked.append((d, lm))

    ranked.sort(key=lambda x: x[0])

    best_distance, best = ranked[0]
    candidates = [
        LandmarkCandidate(
            name=item["name"],
            neighborhood=item["neighborhood"],
            borough=item["borough"],
        )
        for _, item in ranked[:3]
    ]

    if best_distance < 0.5:
        return ResolutionResult(
            status="resolved",
            landmark=best["name"],
            neighborhood=best["neighborhood"],
            borough=best["borough"],
            confidence=0.87,
            candidates=[]
        )

    return ResolutionResult(
        status="needs_clarification",
        confidence=0.42,
        candidates=candidates
    )