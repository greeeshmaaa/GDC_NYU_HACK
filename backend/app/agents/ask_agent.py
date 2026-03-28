from app.models.schemas import AskResponse


def answer_question(landmark: str, question: str, neighborhood: str | None, borough: str | None) -> AskResponse:
    answer = (
        f"You asked about {landmark}. "
        f"This place is important because it connects history, public life, and the identity of "
        f"{neighborhood or borough or 'New York City'}."
    )
    return AskResponse(
        answer_text=answer,
        answer_audio_script=answer,
        followups=[
            "Tell me the story of this place",
            "Show community context",
            "What public resources are nearby?"
        ]
    )