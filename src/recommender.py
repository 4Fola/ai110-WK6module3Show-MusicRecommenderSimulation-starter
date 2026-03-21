# src/recommender.py
from __future__ import annotations
import csv
from typing import Dict, List, Tuple, Optional

# [§Phase 3 – Step 1] CSV loader that casts numerics and parses mood_tags. 
def load_songs(csv_path: str = "data/songs.csv") -> List[Dict]:
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Safe numeric casting
            def _to_float(k, default=0.0):
                try:
                    return float(row.get(k, default)) if row.get(k, "") != "" else default
                except ValueError:
                    return default

            def _to_int(k, default=0):
                try:
                    return int(float(row.get(k, default))) if row.get(k, "") != "" else default
                except ValueError:
                    return default

            row["energy"] = _to_float("energy")
            row["tempo_bpm"] = _to_float("tempo_bpm")
            row["popularity"] = _to_int("popularity")
            row["release_decade"] = _to_int("release_decade")
            # Parse mood_tags into a normalized list
            tags = row.get("mood_tags", "") or ""
            row["mood_tags"] = [t.strip().lower() for t in tags.split(";") if t.strip()] if tags else []
            # Normalize basic strings
            for key in ("title", "artist", "genre", "mood"):
                if key in row and isinstance(row[key], str):
                    row[key] = row[key].strip()
            songs.append(row)
    return songs

# [§Phase 3 – Step 2] Scoring rules with reasons. Modes tweak weights.
def score_song(
    user_prefs: Dict,
    song: Dict,
    mode: str = "balanced",
) -> Tuple[float, List[str]]:
    """
    Returns (score, reasons) for a single song.
    user_prefs keys (minimal): favorite_genre, favorite_mood, target_energy (0..1)
    Optional: target_tempo_bpm (int), desired_mood_tags (list[str])
    """
    reasons: List[str] = []
    # Weight presets (Strategy-like) [§Optional – Challenge 2]
    if mode == "genre_first":
        W = dict(genre=2.5, mood=0.8, energy=1.0, tempo=0.6, tags=0.4, pop=0.4)
    elif mode == "mood_first":
        W = dict(genre=1.0, mood=1.8, energy=1.0, tempo=0.5, tags=1.0, pop=0.4)
    elif mode == "energy_focused":
        W = dict(genre=0.5, mood=0.6, energy=2.5, tempo=1.0, tags=0.2, pop=0.3)
    else:  # balanced (default)
        W = dict(genre=2.0, mood=1.0, energy=1.5, tempo=0.6, tags=0.6, pop=0.5)

    score = 0.0

    # Genre match (exact)
    if user_prefs.get("favorite_genre") and song.get("genre"):
        if song["genre"].lower() == user_prefs["favorite_genre"].lower():
            score += W["genre"]
            reasons.append(f"genre match (+{W['genre']:.1f})")

    # Mood match (exact)
    if user_prefs.get("favorite_mood") and song.get("mood"):
        if song["mood"].lower() == user_prefs["favorite_mood"].lower():
            score += W["mood"]
            reasons.append(f"mood match (+{W['mood']:.1f})")

    # Energy similarity (closer is better) in [0..1]
    if "target_energy" in user_prefs and isinstance(user_prefs["target_energy"], (int, float)):
        gap = abs((song.get("energy") or 0.0) - float(user_prefs["target_energy"]))
        sim = 1.0 - min(max(gap, 0.0), 1.0)  # simple linear similarity
        inc = W["energy"] * sim
        score += inc
        reasons.append(f"energy similarity {sim:.2f} (+{inc:.2f})")

    # Tempo similarity (optional)
    if user_prefs.get("target_tempo_bpm") is not None:
        song_t = float(song.get("tempo_bpm") or 0.0)
        tgt_t = float(user_prefs["target_tempo_bpm"])
        gap = abs(song_t - tgt_t)
        # Normalize by a broad BPM band (200 BPM span)
        sim = 1.0 - min(gap / 200.0, 1.0)
        inc = W["tempo"] * sim
        score += inc
        reasons.append(f"tempo similarity {sim:.2f} (+{inc:.2f})")

    # Mood tag overlaps (optional) [§Optional – Challenge 1]
    desired_tags = [t.strip().lower() for t in user_prefs.get("desired_mood_tags", [])]
    if desired_tags and song.get("mood_tags"):
        overlap = len(set(desired_tags).intersection(set(song["mood_tags"])))
        if overlap > 0:
            inc = W["tags"] * min(overlap, 3) / 3.0  # cap impact
            score += inc
            reasons.append(f"mood tag overlap x{overlap} (+{inc:.2f})")

    # Popularity (mild boost) [§Optional – Challenge 1]
    pop = float(song.get("popularity") or 0.0) / 100.0  # 0..1
    if pop > 0:
        inc = W["pop"] * pop
        score += inc
        reasons.append(f"popularity {pop:.2f} (+{inc:.2f})")

    return score, reasons

# [§Phase 3 – Step 3] Ranking with optional diversity penalty (artist/genre). 
def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 10,
    mode: str = "balanced",
    diversity: bool = True,
) -> List[Dict]:
    # Score all songs first
    scored = []
    for s in songs:
        base, reasons = score_song(user_prefs, s, mode=mode)
        scored.append({
            "song": s,
            "base_score": base,
            "reasons": reasons,
        })

    # Sort by base score (desc), then stable title
    scored.sort(key=lambda x: (x["base_score"], x["song"].get("title", "")), reverse=True)

    if not diversity:
        # Return top-k without diversity penalty
        out = []
        for x in scored[:k]:
            out.append({
                "title": x["song"].get("title"),
                "artist": x["song"].get("artist"),
                "score": round(x["base_score"], 4),
                "reasons": x["reasons"],
            })
        return out

    # Apply diversity penalty greedily [§Optional – Challenge 3]
    taken: List[Dict] = []
    seen_artist: Dict[str, int] = {}
    seen_genre: Dict[str, int] = {}

    remaining = scored.copy()
    while len(taken) < min(k, len(remaining)):
        best_idx = -1
        best_adj = -1e9
        best_entry = None

        for i, entry in enumerate(remaining):
            s = entry["song"]
            artist = (s.get("artist") or "").lower()
            genre = (s.get("genre") or "").lower()
            penalty = 0.15 * seen_artist.get(artist, 0) + 0.10 * seen_genre.get(genre, 0)
            adj = entry["base_score"] - penalty
            if adj > best_adj:
                best_adj = adj
                best_idx = i
                best_entry = {
                    "song": s,
                    "score": round(adj, 4),
                    "reasons": entry["reasons"][:] + ([f"diversity penalty (-{penalty:.2f})"] if penalty > 0 else []),
                }

        # Take best current
        chosen = best_entry
        taken.append({
            "title": chosen["song"].get("title"),
            "artist": chosen["song"].get("artist"),
            "score": chosen["score"],
            "reasons": chosen["reasons"],
        })

        # Update counts and remove chosen from remaining
        artist = (chosen["song"].get("artist") or "").lower()
        genre = (chosen["song"].get("genre") or "").lower()
        seen_artist[artist] = seen_artist.get(artist, 0) + 1
        seen_genre[genre] = seen_genre.get(genre, 0) + 1
        remaining.pop(best_idx)

    return taken


def load_songs(csv_path: str = "data/songs.csv") -> List[Dict]:
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["energy"] = float(row.get("energy") or 0.0)
            row["tempo_bpm"] = float(row.get("tempo_bpm") or 0.0)
            songs.append(row)
    return songs  # [§Phase 3 – Step 1]

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    score = 0.0
    reasons = []
    if song.get("genre","").lower() == user_prefs.get("favorite_genre","").lower():
        score += 2.0; reasons.append("genre match (+2.0)")  # [§Phase 3 – Step 2]
    if song.get("mood","").lower() == user_prefs.get("favorite_mood","").lower():
        score += 1.0; reasons.append("mood match (+1.0)")
    if "target_energy" in user_prefs:
        sim = 1.0 - min(abs(song["energy"] - float(user_prefs["target_energy"])), 1.0)
        inc = 1.5 * sim; score += inc; reasons.append(f"energy similarity {sim:.2f} (+{inc:.2f})")
    if user_prefs.get("target_tempo_bpm") is not None:
        gap = abs(float(song["tempo_bpm"]) - float(user_prefs["target_tempo_bpm"]))
        sim = 1.0 - min(gap/200.0, 1.0)
        inc = 0.6 * sim; score += inc; reasons.append(f"tempo similarity {sim:.2f} (+{inc:.2f})")
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 10) -> List[Dict]:
    scored = []
    for s in songs:
        sc, rs = score_song(user_prefs, s)
        scored.append({"title": s.get("title"), "artist": s.get("artist"), "score": round(sc,4), "reasons": rs})
    return sorted(scored, key=lambda x: x["score"], reverse=True)[:k]  # [§Phase 3 – Step 3]








# from typing import List, Dict, Tuple, Optional
# from dataclasses import dataclass

# @dataclass
# class Song:
#     """
#     Represents a song and its attributes.
#     Required by tests/test_recommender.py
#     """
#     id: int
#     title: str
#     artist: str
#     genre: str
#     mood: str
#     energy: float
#     tempo_bpm: float
#     valence: float
#     danceability: float
#     acousticness: float

# @dataclass
# class UserProfile:
#     """
#     Represents a user's taste preferences.
#     Required by tests/test_recommender.py
#     """
#     favorite_genre: str
#     favorite_mood: str
#     target_energy: float
#     likes_acoustic: bool

# class Recommender:
#     """
#     OOP implementation of the recommendation logic.
#     Required by tests/test_recommender.py
#     """
#     def __init__(self, songs: List[Song]):
#         self.songs = songs

#     def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
#         # TODO: Implement recommendation logic
#         return self.songs[:k]

#     def explain_recommendation(self, user: UserProfile, song: Song) -> str:
#         # TODO: Implement explanation logic
#         return "Explanation placeholder"

# def load_songs(csv_path: str) -> List[Dict]:
#     """
#     Loads songs from a CSV file.
#     Required by src/main.py
#     """
#     # TODO: Implement CSV loading logic
#     print(f"Loading songs from {csv_path}...")
#     return []

# def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
#     """
#     Functional implementation of the recommendation logic.
#     Required by src/main.py
#     """
#     # TODO: Implement scoring and ranking logic
#     # Expected return format: (song_dict, score, explanation)
#     return []
