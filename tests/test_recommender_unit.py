# [Doc §Phase 3 – Step 3] Unit checks: signature, reasons, and diversity behavior.
from src.recommender import recommend_songs

def _mk_song(title, artist, genre="Pop", mood="Happy", energy=0.8, tempo=120, pop=50):
    return {
        "title": title, "artist": artist, "genre": genre, "mood": mood,
        "energy": energy, "tempo_bpm": tempo, "popularity": pop, "mood_tags": []
    }

def test_signature_supports_mode_and_diversity():
    # Minimal in-memory catalog
    songs = [
        _mk_song("A1", "ArtistA"),
        _mk_song("B1", "ArtistB", energy=0.78),
        _mk_song("C1", "ArtistC", energy=0.76),
    ]
    prefs = {
        "favorite_genre": "Pop",
        "favorite_mood": "Happy",
        "target_energy": 0.8,
        "target_tempo_bpm": 120,
        "desired_mood_tags": [],
    }
    out = recommend_songs(prefs, songs, k=3, mode="balanced", diversity=True)
    assert len(out) == 3
    assert isinstance(out[0]["reasons"], list)

def test_diversity_penalty_increases_artist_variety():
    # Three very similar high-score songs by the same artist, plus one by a different artist
    songs = [
        _mk_song("A-top", "ArtistA", energy=0.8),
        _mk_song("A-2",   "ArtistA", energy=0.8),
        _mk_song("A-3",   "ArtistA", energy=0.8),
        _mk_song("B-1",   "ArtistB", energy=0.79),
    ]
    prefs = {
        "favorite_genre": "Pop",
        "favorite_mood": "Happy",
        "target_energy": 0.8,
        "target_tempo_bpm": 120,
        "desired_mood_tags": [],
    }

    out_no_div = recommend_songs(prefs, songs, k=3, mode="balanced", diversity=False)
    out_div    = recommend_songs(prefs, songs, k=3, mode="balanced", diversity=True)

    # Count unique artists
    uniq_no_div = len({x["artist"] for x in out_no_div})
    uniq_div    = len({x["artist"] for x in out_div})

    # With diversity=True we should have >= variety (and typically strictly more)
    assert uniq_div >= uniq_no_div
    assert uniq_div >= 2  # expect at least 2 different artists in top-3

    # It’s also common to observe an explicit penalty reason
    any_penalized = any("diversity penalty" in "; ".join(x["reasons"]) for x in out_div)
    assert any_penalized