# app.py
# [Doc §Optional – Challenge 4] Local-only FastAPI UI with sane defaults.
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.recommender import load_songs, recommend_songs

app = FastAPI(title="VibeCraft 1.0")  # naming
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

SONGS = load_songs()  # load once

# Will supply defaults on index so template never sees missing vars (prevents blank/undefined).
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    default_prefs = {
        "favorite_genre": "",
        "favorite_mood": "",
        "target_energy": 0.70,
        "target_tempo_bpm": 120,
        "desired_mood_tags": [],
    }
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "genres": sorted({s.get("genre") for s in SONGS if s.get("genre")}),
            "moods": sorted({s.get("mood") for s in SONGS if s.get("mood")}),
            "results": [],
            "prefs": default_prefs,
            "mode": "balanced",
            "top_k": 10,              # [Preferences]
            "diversity": True,
        },
    )

@app.get("/recommend", response_class=HTMLResponse)
async def recommend(
    request: Request,
    favorite_genre: str = "",
    favorite_mood: str = "",
    target_energy: float = 0.7,
    target_tempo_bpm: int = 120,
    desired_mood_tags: str = "",
    mode: str = "balanced",
    top_k: int = 10,
    diversity: bool = True,
):
    # Input clamping (local only but keeping it clean)
    try:
        target_energy = max(0.0, min(1.0, float(target_energy)))
    except Exception:
        target_energy = 0.7
    try:
        target_tempo_bpm = max(40, min(200, int(target_tempo_bpm)))
    except Exception:
        target_tempo_bpm = 120
    try:
        top_k = max(1, min(20, int(top_k)))
    except Exception:
        top_k = 10

    desired_tags = [t.strip() for t in desired_mood_tags.split(",") if t.strip()]
    prefs = {
        "favorite_genre": favorite_genre.strip(),
        "favorite_mood": favorite_mood.strip(),
        "target_energy": target_energy,
        "target_tempo_bpm": target_tempo_bpm,
        "desired_mood_tags": desired_tags,
    }

    recs = recommend_songs(prefs, SONGS, k=top_k, mode=mode, diversity=diversity)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "genres": sorted({s.get("genre") for s in SONGS if s.get("genre")}),
            "moods": sorted({s.get("mood") for s in SONGS if s.get("mood")}),
            "results": recs,
            "prefs": prefs,
            "mode": mode,
            "top_k": top_k,
            "diversity": diversity,
        },
    )