import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(filename: str):
    path = DATA_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_landmarks():
    return load_json("landmarks.json")


def get_community_profiles():
    return load_json("community_profiles.json")


def get_profile_for_landmark(landmark_name: str):
    profiles = get_community_profiles()
    return profiles.get(landmark_name, {})