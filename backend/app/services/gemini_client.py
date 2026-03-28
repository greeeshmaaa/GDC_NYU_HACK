import os
import json
import base64
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL_NAME = os.getenv("VERTEX_MODEL", "gemini-2.5-flash")

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
)


def detect_landmark_from_image_open(image_base64: str) -> dict:
    if image_base64.startswith("data:image"):
        image_base64 = image_base64.split(",", 1)[1]

    image_bytes = base64.b64decode(image_base64)

    prompt = """
You are a landmark recognition system for a New York City app.

Look at the image and identify the most likely famous landmark shown.

Rules:
- If you can identify a landmark, return its most standard landmark name.
- Prefer concise names like:
  - Brooklyn Bridge
  - Grand Central Terminal
  - Apollo Theater
- If unclear, return landmark as null.
- Confidence must be from 0.0 to 1.0.
- Return JSON only.

Return exactly:
{
  "landmark": "Brooklyn Bridge" or null,
  "confidence": 0.0,
  "reason": "short explanation"
}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            prompt,
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
        ],
        config=types.GenerateContentConfig(
            temperature=0.0,
            response_mime_type="application/json",
        ),
    )

    print("Raw Gemini response text:", response.text)
    return json.loads(response.text)