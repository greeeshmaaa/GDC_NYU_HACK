from app.models.schemas import ResolutionResult


def build_clarification_prompt(resolution: ResolutionResult) -> dict:
    if resolution.status != "needs_clarification":
        return {"message": None, "options": []}

    options = [c.name for c in resolution.candidates]
    if len(options) == 1:
        message = f"I think you may be near {options[0]}. Is that correct?"
    else:
        joined = ", ".join(options)
        message = f"I couldn't confidently identify the exact landmark. Are you at {joined}?"
    return {
        "message": message,
        "options": options
    }