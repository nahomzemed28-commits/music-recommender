"""
Command line runner for the Music Recommender Simulation.

Run with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs

# ---------------------------------------------------------------------------
# User Profiles
# ---------------------------------------------------------------------------

HAPPY_POP = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.82,
    "likes_acoustic": False,
}

CHILL_LOFI = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.38,
    "likes_acoustic": True,
}

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

    genre = user_prefs["favorite_genre"].title()
    mood  = user_prefs["favorite_mood"].title()
    print(f"Top 5 Recommendations for {genre} / {mood} listener")
    print("=" * 50)

    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{i}. {song['title']}  —  {song['artist']}  [{song['genre']}]")
        print(f"   Score : {score:.2f}")
        print(f"   Why   : {explanation}")

    print()


if __name__ == "__main__":
    main()
