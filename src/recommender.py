from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to int/float."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song 0–4.5 pts using genre (+2.0), mood (+1.0), energy (+1.0), and acousticness (+0.5) signals; return (score, reasons)."""
    score = 0.0
    reasons = []

    # Genre match (+2.0)
    if song["genre"] == user_prefs["genre"]:
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    # Mood match (+1.0)
    if song["mood"] == user_prefs["mood"]:
        score += 1.0
        reasons.append(f"mood match (+1.0)")

    # Energy proximity (+1.0 × proximity)
    energy_proximity = 1.0 - abs(user_prefs["target_energy"] - song["energy"])
    score += 1.0 * energy_proximity
    reasons.append(f"energy proximity (+{1.0 * energy_proximity:.2f})")

    # Acousticness proximity (+0.5 × proximity)
    target_acousticness = 0.8 if user_prefs["likes_acoustic"] else 0.2
    acousticness_proximity = 1.0 - abs(target_acousticness - song["acousticness"])
    score += 0.5 * acousticness_proximity
    reasons.append(f"acousticness proximity (+{0.5 * acousticness_proximity:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort descending, and return the top-k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: (x[1], -abs(user_prefs["target_energy"] - x[0]["energy"])), reverse=True)
    return scored[:k]
