"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from typing import Dict, List, Tuple

from src.recommender import load_songs, recommend_songs


def print_recommendations(
    label: str,
    user_prefs: Dict[str, object],
    songs: List[Dict[str, object]],
) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\n=== {label} ===")
    print(f"Profile: {user_prefs}")
    print("Top recommendations:\n")

    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        reasons = explanation.split("; ") if explanation else ["no reasons available"]

        print(f"{rank}. {song['title']} - Score: {score:.2f}")
        print(f"   Artist: {song['artist']}")
        print("   Reasons:")
        for reason in reasons:
            print(f"   - {reason}")
        print()


def main() -> None:
    songs: List[Dict[str, object]] = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles: List[Tuple[str, Dict[str, object]]] = [
        (
            "High-Energy Pop",
            {"genre": "pop", "mood": "happy", "energy": 0.9, "likes_acoustic": False},
        ),
        (
            "Chill Lofi",
            {"genre": "lofi", "mood": "chill", "energy": 0.3, "likes_acoustic": True},
        ),
        (
            "Deep Intense Rock",
            {"genre": "rock", "mood": "intense", "energy": 0.85, "likes_acoustic": False},
        ),
        (
            "Adversarial Conflicted",
            {"genre": "experimental_noise", "mood": "sad", "energy": 0.9, "likes_acoustic": True},
        ),
        (
            "Retro Nostalgia",
            {
                "genre": "synthwave",
                "mood": "moody",
                "energy": 0.72,
                "likes_acoustic": False,
                "preferred_decade": 1980,
                "desired_mood_tag": "nostalgic",
                "target_popularity": 70,
                "target_aggressiveness": 0.4,
                "likes_synth": True,
                "likes_nostalgia": True,
            },
        ),
    ]

    for label, user_prefs in profiles:
        print_recommendations(label, user_prefs, songs)


if __name__ == "__main__":
    main()
