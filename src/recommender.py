from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

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
        scored_songs = sorted(
            self.songs,
            key=lambda song: score_song(
                {
                    "genre": user.favorite_genre,
                    "mood": user.favorite_mood,
                    "energy": user.target_energy,
                    "likes_acoustic": user.likes_acoustic,
                },
                _song_to_dict(song),
            )[0],
            reverse=True,
        )
        return scored_songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = score_song(
            {
                "genre": user.favorite_genre,
                "mood": user.favorite_mood,
                "energy": user.target_energy,
                "likes_acoustic": user.likes_acoustic,
            },
            _song_to_dict(song),
        )
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": int(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            }
            songs.append(song)

    return songs


def _song_to_dict(song: Song) -> Dict:
    """Convert a Song dataclass into a dictionary."""
    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "genre": song.genre,
        "mood": song.mood,
        "energy": song.energy,
        "tempo_bpm": song.tempo_bpm,
        "valence": song.valence,
        "danceability": song.danceability,
        "acousticness": song.acousticness,
    }


def _get_value(item: Dict, *keys: str):
    """Return the first matching value for a list of possible keys."""
    for key in keys:
        if key in item:
            return item[key]
    return None


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song and return its numeric score plus reasons."""
    score = 0.0
    reasons: List[str] = []

    user_genre = _get_value(user_prefs, "genre", "favorite_genre")
    user_mood = _get_value(user_prefs, "mood", "favorite_mood")
    user_energy = _get_value(user_prefs, "energy", "target_energy")
    likes_acoustic = bool(_get_value(user_prefs, "likes_acoustic"))

    if user_genre and song.get("genre") == user_genre:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if user_mood and song.get("mood") == user_mood:
        score += 1.0
        reasons.append("mood match (+1.0)")

    if user_energy is not None and song.get("energy") is not None:
        distance = abs(float(song["energy"]) - float(user_energy))
        energy_points = max(0.0, 1.5 * (1.0 - distance))
        score += energy_points
        reasons.append(f"energy close to target (+{energy_points:.2f})")

    acousticness = song.get("acousticness")
    if acousticness is not None:
        if likes_acoustic:
            acoustic_points = 0.5 * float(acousticness)
            score += acoustic_points
            reasons.append(f"acoustic sound bonus (+{acoustic_points:.2f})")
        else:
            acoustic_points = -0.5 * float(acousticness)
            score += acoustic_points
            reasons.append(f"less acoustic preference ({acoustic_points:.2f})")

    if not reasons:
        reasons.append("no strong matches")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank songs by score and return the top k results."""
    scored_songs = [
        (song, score, "; ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    return sorted(scored_songs, key=lambda item: item[1], reverse=True)[:k]
