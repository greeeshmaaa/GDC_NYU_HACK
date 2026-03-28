from app.models.schemas import CommunityResponse
from app.services.dataset_service import get_profile_for_landmark


def get_community_context(landmark: str) -> CommunityResponse:
    profile = get_profile_for_landmark(landmark)

    return CommunityResponse(
        community_summary=profile.get(
            "community_summary",
            "This place connects to public life through nearby resources and civic infrastructure."
        ),
        nearby_resources=profile.get("nearby_resources", []),
        environmental_context=profile.get("environmental_context", []),
        helpful_actions=profile.get("helpful_actions", [])
    )