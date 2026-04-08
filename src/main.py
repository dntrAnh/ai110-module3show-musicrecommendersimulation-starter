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


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Taste profile used for content-based scoring.
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.82,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n=== Top Recommendations ===\n")
    for idx, (song, score, explanation) in enumerate(recommendations, start=1):
        reasons = [part.strip() for part in explanation.split(",") if part.strip()]
        print(f"{idx}. {song['title']} — {song['artist']}")
        print(f"   Score   : {score:.2f}")
        print("   Reasons :")
        for reason in reasons:
            print(f"   - {reason}")
        print()


if __name__ == "__main__":
    main()
