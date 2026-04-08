"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    # Works when run as a module: python -m src.main
    from .recommender import load_songs, recommend_songs
except ImportError:
    # Works when run as a script: python src/main.py
    from recommender import load_songs, recommend_songs


def print_recommendations_for_profile(profile_name: str, user_prefs: dict, songs: list) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\n=== {profile_name} ===")
    print(f"Preferences: {user_prefs}\n")

    for idx, (song, score, explanation) in enumerate(recommendations, start=1):
        reasons = [part.strip() for part in explanation.split(",") if part.strip()]
        print(f"{idx}. {song['title']} - {song['artist']}")
        print(f"   Score   : {score:.2f}")
        print("   Reasons :")
        for reason in reasons:
            print(f"   - {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    baseline_profiles = [
        (
            "High-Energy Pop",
            {
                "genre": "pop",
                "mood": "happy",
                "energy": 0.90,
            },
        ),
        (
            "Chill Lofi",
            {
                "genre": "lofi",
                "mood": "calm",
                "energy": 0.30,
            },
        ),
        (
            "Deep Intense Rock",
            {
                "genre": "rock",
                "mood": "intense",
                "energy": 0.88,
            },
        ),
    ]

    adversarial_profiles = [
        (
            "Conflicting Preferences (High Energy + Sad Mood)",
            {
                "genre": "pop",
                "mood": "sad",
                "energy": 0.90,
            },
        ),
        (
            "Sparse Profile (Genre Only)",
            {
                "genre": "rock",
            },
        ),
        (
            "Boundary Energy Tie Case",
            {
                "genre": "pop",
                "mood": "happy",
                "energy": 0.50,
            },
        ),
    ]

    print("\n=== Stress Test: Diverse and Adversarial User Profiles ===")
    for profile_name, user_prefs in baseline_profiles + adversarial_profiles:
        print_recommendations_for_profile(profile_name, user_prefs, songs)


if __name__ == "__main__":
    main()
