from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.schemas import (
    CaptureRequest,
    ClarifyRequest,
    AskRequest,
    StoryRequest,
    CommunityRequest,
)
from app.agents.landmark_agent import detect_landmark
from app.agents.clarifying_agent import build_clarification_prompt
from app.agents.ask_agent import answer_question
from app.agents.story_agent import generate_story
from app.agents.community_agent import get_community_context
from app.agents.narrator_agent import build_mode_summary

app = FastAPI(title="NYC Lens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/capture")
def capture_landmark(payload: CaptureRequest):
    resolution = detect_landmark(payload.image_base64, payload.lat, payload.lng)

    if resolution.status == "needs_clarification":
        clarify = build_clarification_prompt(resolution)
        return {
            "status": "needs_clarification",
            "clarification": clarify
        }

    summary = build_mode_summary(
        resolution.landmark,
        resolution.neighborhood,
        resolution.borough
    )

    return {
        "status": "resolved",
        "place": resolution.model_dump(),
        "summary": summary,
        "available_modes": ["ask", "story", "community"]
    }


@app.post("/clarify")
def clarify_place(payload: ClarifyRequest):
    return {
        "status": "resolved",
        "place": {
            "landmark": payload.selected_place,
            "confidence": 1.0,
            "status": "resolved"
        },
        "available_modes": ["ask", "story", "community"]
    }


@app.post("/ask")
def ask_mode(payload: AskRequest):
    return answer_question(
        landmark=payload.landmark,
        question=payload.question,
        neighborhood=payload.neighborhood,
        borough=payload.borough
    )


@app.post("/story")
def story_mode(payload: StoryRequest):
    return generate_story(
        landmark=payload.landmark,
        neighborhood=payload.neighborhood,
        borough=payload.borough
    )


@app.post("/community")
def community_mode(payload: CommunityRequest):
    return get_community_context(payload.landmark)