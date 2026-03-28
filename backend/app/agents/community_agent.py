from math import radians, cos, sin, asin, sqrt
from app.models.schemas import CommunityResponse
from app.services.dataset_service import get_unified_places, get_landmark_by_name


def haversine(lat1, lon1, lat2, lon2):
    if None in [lat1, lon1, lat2, lon2]:
        return float("inf")
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return 6371 * c


def get_community_context(landmark: str) -> CommunityResponse:
    landmark_data = get_landmark_by_name(landmark)
    unified_places = get_unified_places()

    if not landmark_data:
        return CommunityResponse(
            community_summary="This place connects to public life through nearby resources and civic infrastructure.",
            nearby_resources=[],
            environmental_context=[],
            helpful_actions=[]
        )

    lat = landmark_data.get("lat")
    lng = landmark_data.get("lng")

    nearby = []
    for place in unified_places:
        d = haversine(lat, lng, place.get("lat"), place.get("lng"))
        if d <= 1.0:
            nearby.append((d, place))

    nearby.sort(key=lambda x: x[0])
    top_nearby = [item for _, item in nearby[:8]]

    nearby_resources = []
    environmental_context = []
    helpful_actions = []

    for item in top_nearby:
        subtype = item.get("subtype")
        name = item.get("name")

        if subtype == "park":
            nearby_resources.append(f"{name} nearby")
            environmental_context.append("Nearby green/open public space is available.")
        else:
            nearby_resources.append(f"{name} nearby")

    helpful_actions = [
        "Explore nearby public spaces",
        "Find nearby civic places",
        "Learn more about this landmark"
    ]

    summary = "This landmark connects to public life through nearby places and public-interest resources."

    return CommunityResponse(
        community_summary=summary,
        nearby_resources=nearby_resources[:5],
        environmental_context=list(dict.fromkeys(environmental_context))[:3],
        helpful_actions=helpful_actions
    )