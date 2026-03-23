# [Doc §Phase 4 – Step 1] API smoke tests (keeps signature & routing healthy).
import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app from the project root
from app import app

client = TestClient(app)

def test_index_ok():
    r = client.get("/")
    assert r.status_code == 200
    # Basic marker text rendered by the template
    assert "COdePath VibeCraft 1.0" in r.text

def test_recommend_ok_top3_balanced():
    params = {
        "favorite_genre": "Pop",
        "favorite_mood": "Happy",
        "target_energy": 0.8,
        "target_tempo_bpm": 120,
        "desired_mood_tags": "anthem,euphoric",
        "mode": "balanced",
        "top_k": 3,
        "diversity": True,
    }
    r = client.get("/recommend", params)