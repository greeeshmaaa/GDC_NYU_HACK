import re
from math import radians, cos, sin, asin, sqrt
from difflib import get_close_matches

from app.models.schemas import ResolutionResult, LandmarkCandidate
from app.services.dataset_service import get_landmark_context
from app.services.gemini_client import detect_landmark_from_image_open


def haversine(lat1, lon1, lat2, lon2):
    if None in [lat1, lon1, lat2, lon2]:
        return float("inf")
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return 6371 * c


def normalize_name(name: str) -> str:
    if not name:
        return ""
    name = name.lower().strip()
    name = re.sub(r"[^a-z0-9\s]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name


def build_name_index(landmark_context: dict):
    index = {}
    for original_name in landmark_context.keys():
        index[normalize_name(original_name)] = original_name
    return index


def resolve_landmark_name(guessed_name: str, landmark_context: dict) -> str | None:
    if not guessed_name:
        return None

    normalized_guess = normalize_name(guessed_name)
    index = build_name_index(landmark_context)

    print("Guessed landmark raw:", guessed_name)
    print("Guessed landmark normalized:", normalized_guess)

    if normalized_guess in index:
        print("Exact normalized match found:", index[normalized_guess])
        return index[normalized_guess]

    matches = get_close_matches(normalized_guess, list(index.keys()), n=3, cutoff=0.60)
    print("Closest fuzzy matches:", matches)

    if matches:
        print("Resolved via fuzzy match:", index[matches[0]])
        return index[matches[0]]

    print("No landmark match found in dataset.")
    return None


def build_geo_clarification_candidates(lat: float | None, lng: float | None, landmark_context: dict):
    ranked = []
    for landmark_name, landmark_data in landmark_context.items():
        lm_lat = landmark_data.get("lat")
        lm_lng = landmark_data.get("lng")
        distance = haversine(lat, lng, lm_lat, lm_lng)
        ranked.append((distance, landmark_name, landmark_data))

    ranked.sort(key=lambda x: x[0])
    top_matches = ranked[:3]

    candidates = [
        LandmarkCandidate(
            name=name,
            neighborhood=None,
            borough=data.get("borough"),
        )
        for _, name, data in top_matches
    ]

    return candidates


def detect_landmark(image_base64: str, lat: float | None, lng: float | None) -> ResolutionResult:
    landmark_context = get_landmark_context()

    try:
        gemini_result = detect_landmark_from_image_open(image_base64)
        print("Gemini open landmark result:", gemini_result)

        guessed_name = gemini_result.get("landmark")
        confidence = float(gemini_result.get("confidence", 0.0) or 0.0)

        print("Gemini guessed_name:", guessed_name)
        print("Gemini confidence:", confidence)

        matched_landmark = resolve_landmark_name(guessed_name, landmark_context)
        print("Matched landmark in dataset:", matched_landmark)

        # TEMP: lower threshold for debugging
        if matched_landmark and confidence >= 0.50:
            data = landmark_context.get(matched_landmark, {})
            print("Returning RESOLVED:", matched_landmark)
            return ResolutionResult(
                status="resolved",
                landmark=matched_landmark,
                neighborhood=None,
                borough=data.get("borough"),
                confidence=confidence,
                candidates=[]
            )

        print("Image-first detection did not meet threshold or failed to match dataset.")

    except Exception as e:
        print("Gemini image-first landmark detection failed:", str(e))

    print("Falling back to clarification candidates from geolocation.")
    candidates = build_geo_clarification_candidates(lat, lng, landmark_context)

    return ResolutionResult(
        status="needs_clarification",
        confidence=0.40,
        candidates=candidates
    )