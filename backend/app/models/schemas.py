from typing import List, Optional, Literal
from pydantic import BaseModel


class LandmarkCandidate(BaseModel):
    name: str
    neighborhood: Optional[str] = None
    borough: Optional[str] = None


class CaptureRequest(BaseModel):
    image_base64: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    heading: Optional[float] = None


class ResolutionResult(BaseModel):
    status: Literal["resolved", "needs_clarification"]
    landmark: Optional[str] = None
    neighborhood: Optional[str] = None
    borough: Optional[str] = None
    confidence: float = 0.0
    candidates: List[LandmarkCandidate] = []


class ClarifyRequest(BaseModel):
    selected_place: str
    lat: Optional[float] = None
    lng: Optional[float] = None


class AskRequest(BaseModel):
    landmark: str
    neighborhood: Optional[str] = None
    borough: Optional[str] = None
    question: str


class AskResponse(BaseModel):
    answer_text: str
    answer_audio_script: str
    followups: List[str]


class StoryRequest(BaseModel):
    landmark: str
    neighborhood: Optional[str] = None
    borough: Optional[str] = None


class StoryResponse(BaseModel):
    title: str
    story_beats: List[str]
    highlighted_fact: str
    why_it_still_matters: str
    audio_script: str


class CommunityRequest(BaseModel):
    landmark: str
    neighborhood: Optional[str] = None
    borough: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class CommunityResponse(BaseModel):
    community_summary: str
    nearby_resources: List[str]
    environmental_context: List[str]
    helpful_actions: List[str]