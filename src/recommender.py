from typing import Any, List, Dict, Tuple, Optional
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
    popularity: Optional[int] = None
    release_decade: Optional[int] = None
    mood_tag: Optional[str] = None
    aggressiveness: Optional[float] = None
    synthiness: Optional[float] = None
    nostalgia_score: Optional[float] = None

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

def load_songs(csv_path: str) -> List[Dict[str, Any]]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict[str, Any]] = []

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            song: Dict[str, Any] = {
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
                "popularity": int(row.get("popularity", 0)) if row.get("popularity") else None,
                "release_decade": int(row.get("release_decade", 0)) if row.get("release_decade") else None,
                "mood_tag": row.get("mood_tag") or None,
                "aggressiveness": float(row["aggressiveness"]) if row.get("aggressiveness") else None,
                "synthiness": float(row["synthiness"]) if row.get("synthiness") else None,
                "nostalgia_score": float(row["nostalgia_score"]) if row.get("nostalgia_score") else None,
            }
            songs.append(song)

    return songs


def _song_to_dict(song: Song) -> Dict[str, Any]:
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
        "popularity": song.popularity,
        "release_decade": song.release_decade,
        "mood_tag": song.mood_tag,
        "aggressiveness": song.aggressiveness,
        "synthiness": song.synthiness,
        "nostalgia_score": song.nostalgia_score,
    }


def _get_value(item: Dict[str, Any], *keys: str) -> Any:
    """Return the first matching value for a list of possible keys."""
    for key in keys:
        if key in item:
            return item[key]
    return None


def score_song(user_prefs: Dict[str, Any], song: Dict[str, Any]) -> Tuple[float, List[str]]:
    """Score one song and return its numeric score plus reasons."""
    score = 0.0
    reasons: List[str] = []

    user_genre = _get_value(user_prefs, "genre", "favorite_genre")
    user_mood = _get_value(user_prefs, "mood", "favorite_mood")
    user_energy = _get_value(user_prefs, "energy", "target_energy")
    likes_acoustic = bool(_get_value(user_prefs, "likes_acoustic"))
    preferred_decade = _get_value(user_prefs, "preferred_decade")
    desired_mood_tag = _get_value(user_prefs, "desired_mood_tag", "preferred_mood_tag")
    target_popularity = _get_value(user_prefs, "target_popularity")
    target_aggressiveness = _get_value(user_prefs, "target_aggressiveness")
    likes_synth = _get_value(user_prefs, "likes_synth")
    likes_nostalgia = _get_value(user_prefs, "likes_nostalgia")

    if user_genre and song.get("genre") == user_genre:
        score += 1.0
        reasons.append("genre match (+1.0)")

    if user_mood and song.get("mood") == user_mood:
        score += 1.0
        reasons.append("mood match (+1.0)")

    if user_energy is not None and song.get("energy") is not None:
        distance = abs(float(song["energy"]) - float(user_energy))
        energy_points = max(0.0, 3.0 * (1.0 - distance))
        score += energy_points
        reasons.append(f"energy close to target (+{energy_points:.2f})")

    popularity = song.get("popularity")
    if popularity is not None:
        popularity_points = 0.6 * (max(0.0, min(100.0, float(popularity))) / 100.0)
        score += popularity_points
        reasons.append(f"popularity bonus (+{popularity_points:.2f})")

    release_decade = song.get("release_decade")
    if preferred_decade is not None and release_decade is not None:
        decade_gap = abs(int(release_decade) - int(preferred_decade)) // 10
        decade_points = max(0.0, 1.2 - (0.4 * decade_gap))
        score += decade_points
        reasons.append(f"era match (+{decade_points:.2f})")

    if desired_mood_tag and song.get("mood_tag") == desired_mood_tag:
        mood_tag_points = 1.0
        score += mood_tag_points
        reasons.append("detailed mood tag match (+1.0)")

    aggressiveness = song.get("aggressiveness")
    if target_aggressiveness is not None and aggressiveness is not None:
        aggression_distance = abs(float(aggressiveness) - float(target_aggressiveness))
        aggressiveness_points = max(0.0, 1.5 * (1.0 - aggression_distance))
        score += aggressiveness_points
        reasons.append(f"aggressiveness match (+{aggressiveness_points:.2f})")

    synthiness = song.get("synthiness")
    if synthiness is not None and likes_synth is not None:
        synth_amount = float(synthiness)
        if bool(likes_synth):
            synth_points = 0.5 * synth_amount
            score += synth_points
            reasons.append(f"synth bonus (+{synth_points:.2f})")
        else:
            synth_points = -0.3 * synth_amount
            score += synth_points
            reasons.append(f"less synth preference ({synth_points:.2f})")

    nostalgia_score = song.get("nostalgia_score")
    if nostalgia_score is not None and likes_nostalgia is not None:
        if bool(likes_nostalgia):
            nostalgia_points = 0.8 * float(nostalgia_score)
            score += nostalgia_points
            reasons.append(f"nostalgia bonus (+{nostalgia_points:.2f})")
        else:
            nostalgia_points = -0.2 * float(nostalgia_score)
            score += nostalgia_points
            reasons.append(f"less nostalgia preference ({nostalgia_points:.2f})")

    if target_popularity is not None and popularity is not None:
        popularity_distance = abs(float(popularity) - float(target_popularity)) / 100.0
        popularity_target_points = max(0.0, 0.8 * (1.0 - popularity_distance))
        score += popularity_target_points
        reasons.append(f"popularity preference match (+{popularity_target_points:.2f})")

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

def recommend_songs(
    user_prefs: Dict[str, Any],
    songs: List[Dict[str, Any]],
    k: int = 5,
) -> List[Tuple[Dict[str, Any], float, str]]:
    """Rank songs by score and return the top k results."""
    scored_songs = [
        (song, score, "; ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    return sorted(scored_songs, key=lambda item: item[1], reverse=True)[:k]
