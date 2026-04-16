"""
Command line runner for the Music Recommender Simulation.

Run with:
    python -m src.main

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

# ---------------------------------------------------------------------------
# User Profiles
# Each profile is a dictionary of taste preferences that drives scoring.
# Phase 4 will stress-test all three profiles against the full catalog.
# ---------------------------------------------------------------------------

# Profile 1 — Happy Pop fan: wants bright, high-energy, danceable tracks
HAPPY_POP = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.82,
    "likes_acoustic": False,
}

# Profile 2 — Chill Lofi listener: wants calm, low-energy, acoustic study music
CHILL_LOFI = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.38,
    "likes_acoustic": True,
}

# Profile 3 — Deep Intense Rock fan: wants aggressive, high-energy guitar-driven tracks
INTENSE_ROCK = {
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.90,
    "likes_acoustic": False,
}

# Active profile — change this to switch between profiles
user_prefs = HAPPY_POP


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("Top recommendations:\n")
    for rec in recommendations:
        # Each item returned by recommend_songs is: (song_dict, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
