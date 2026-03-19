# src/main.py
from __future__ import annotations
from .recommender import load_songs, recommend_songs

# [§Phase 4 – Step 1] Multiple user profiles for evaluation. 
USER_PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "Pop",
        "favorite_mood": "Happy",
        "target_energy": 0.85,
        "target_tempo_bpm": 120,
        "desired_mood_tags": ["anthem", "euphoric", "uplifting"],
    },
    "Chill Lofi": {
        "favorite_genre": "Lo-fi",
        "favorite_mood": "Calm",
        "target_energy": 0.30,
        "target_tempo_bpm": 75,
        "desired_mood_tags": ["study", "lofi", "warm", "soothing"],
    },
    "Deep Intense Rock": {
        "favorite_genre": "Rock",
        "favorite_mood": "Intense",
        "target_energy": 0.90,
        "target_tempo_bpm": 150,
        "desired_mood_tags": ["guitar", "aggressive", "anthem"],
    },
}

def print_block(title: str):
    print("=" * 72)
    print(title)
    print("=" * 72)

def main():
    songs = load_songs()
    print_block(f"Loaded songs: {len(songs)}  [Doc §Phase 3 – Step 1]")

    modes = ["balanced", "genre_first", "mood_first", "energy_focused"]
    k = 10  # As requested

    for profile_name, prefs in USER_PROFILES.items():
        for mode in modes:
            print_block(f"{profile_name}  |  mode={mode}  |  top={k}")
            results = recommend_songs(prefs, songs, k=k, mode=mode, diversity=True)
            for idx, r in enumerate(results, 1):
                short_reasons = "; ".join(r["reasons"])
                print(f"{idx:>2}. {r['title']} – {r['artist']}  |  score={r['score']:.3f}")
                print(f"    reasons: {short_reasons}")
            print()

if __name__ == "__main__":
    main()






# """
# Command line runner for the Music Recommender Simulation.

# This file helps you quickly run and test your recommender.

# You will implement the functions in recommender.py:
# - load_songs
# - score_song
# - recommend_songs
# """

# from .recommender import load_songs, recommend_songs


# def main() -> None:
#     songs = load_songs("data/songs.csv") 

#     # Starter example profile
#     user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

#     recommendations = recommend_songs(user_prefs, songs, k=5)

#     print("\nTop recommendations:\n")
#     for rec in recommendations:
#         # You decide the structure of each returned item.
#         # A common pattern is: (song, score, explanation)
#         song, score, explanation = rec
#         print(f"{song['title']} - Score: {score:.2f}")
#         print(f"Because: {explanation}")
#         print()


# if __name__ == "__main__":
#     main()
