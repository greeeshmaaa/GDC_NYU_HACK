def build_mode_summary(landmark: str, neighborhood: str | None, borough: str | None) -> str:
    place_bits = [bit for bit in [landmark, neighborhood, borough] if bit]
    place = ", ".join(place_bits)
    return f"You’re looking at {place}. You can ask questions, explore its story, or discover its community context."