"""
Music Recommender — core logic.

Three responsibilities:
  1. load_songs        — parse the CSV catalog into structured data
  2. score_song        — judge a single song against a user's taste profile
  3. recommend_songs   — rank the full catalog and return the top-k picks

Also exposes Song, UserProfile, and Recommender for the OOP test suite.
"""

import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its audio attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a listener's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP wrapper around the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs sorted by relevance score for this user."""
        return sorted(self.songs, key=lambda song: self._score(user, song), reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language explanation of why this song was recommended."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append("genre match (+2.0)")
        if song.mood == user.favorite_mood:
            reasons.append("mood match (+1.0)")
        energy_score = 1.0 - abs(song.energy - user.target_energy)
        reasons.append(f"energy similarity (+{energy_score:.2f})")
        if user.likes_acoustic and song.acousticness > 0.6:
            reasons.append("acoustic match (+0.5)")
        return ", ".join(reasons) if reasons else "no strong match found"

    def _score(self, user: UserProfile, song: Song) -> float:
        """Compute the numeric relevance score for a Song object."""
        score = 0.0
        if song.genre == user.favorite_genre:
            score += 2.0
        if song.mood == user.favorite_mood:
            score += 1.0
        score += 1.0 - abs(song.energy - user.target_energy)
        if user.likes_acoustic and song.acousticness > 0.6:
            score += 0.5
        return score


# ---------------------------------------------------------------------------
# Functional API (used by src/main.py)
# ---------------------------------------------------------------------------

def load_songs(filepath: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of song dictionaries.

    Numeric fields are cast to the correct Python types so arithmetic
    works correctly in score_song.
    """
    songs = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = int(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against the user's taste profile.

    Algorithm Recipe:
      +2.0  if genre matches user's favorite_genre
      +1.0  if mood  matches user's favorite_mood
      +proximity  where proximity = 1.0 - abs(song_energy - target_energy)
      +0.5  if user likes_acoustic and song acousticness > 0.6

    Returns:
        (total_score, reasons) — reasons is a list of human-readable strings
        explaining exactly what contributed to the score.
    """
    score = 0.0
    reasons = []

    # Genre match — weighted highest: genre is the strongest vibe signal
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match
    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy proximity — rewards closeness, not just higher or lower
    energy_proximity = 1.0 - abs(song["energy"] - user_prefs["target_energy"])
    score += energy_proximity
    reasons.append(f"energy similarity (+{energy_proximity:.2f})")

    # Acoustic bonus
    if user_prefs.get("likes_acoustic", False) and song["acousticness"] > 0.6:
        score += 0.5
        reasons.append("acoustic match (+0.5)")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank all songs and return the top-k recommendations.

    Uses score_song as the judge for every song, then sorts with sorted()
    (non-mutating) so the original catalog list is never modified.

    Returns:
        List of (song_dict, score, explanation) tuples, highest score first.
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
