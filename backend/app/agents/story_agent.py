from app.models.schemas import StoryResponse


def generate_story(landmark: str, neighborhood: str | None, borough: str | None) -> StoryResponse:
    if landmark == "Brooklyn Bridge":
        beats = [
            "Before the bridge, crossing between Manhattan and Brooklyn was slower and less predictable.",
            "When the bridge opened, it transformed movement, commerce, and daily life across the city.",
            "Over time it became both infrastructure and symbol — a landmark of connection and ambition."
        ]
        return StoryResponse(
            title="When the Bridge Changed the City",
            story_beats=beats,
            highlighted_fact="The bridge dramatically reshaped how people and goods moved across the East River.",
            why_it_still_matters="It still represents public connection, mobility, and the scale of city-building.",
            audio_script="Before the bridge, crossing was slower and uncertain. When it opened, it transformed movement and commerce. Today, it remains a symbol of connection."
        )

    return StoryResponse(
        title=f"The Story of {landmark}",
        story_beats=[
            f"{landmark} grew into a meaningful part of {neighborhood or 'the city'}.",
            "Its role expanded through public life, architecture, and memory.",
            "Today, it remains part of the city’s shared identity."
        ],
        highlighted_fact=f"{landmark} continues to hold cultural and civic significance.",
        why_it_still_matters="It helps people connect the city’s past to its present.",
        audio_script=f"{landmark} is more than a structure. It is a living part of the city's memory."
    )