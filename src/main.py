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


def _truncate(text: str, max_len: int) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def _print_recommendations_table(recommendations: list) -> None:
    rows = []
    for idx, (song, score, explanation) in enumerate(recommendations, start=1):
        rows.append(
            {
                "rank": str(idx),
                "title": _truncate(str(song["title"]), 22),
                "artist": _truncate(str(song["artist"]), 18),
                "score": f"{score:.2f}",
                "reasons": _truncate(str(explanation), 92),
            }
        )

    columns = [
        ("rank", "#"),
        ("title", "Title"),
        ("artist", "Artist"),
        ("score", "Score"),
        ("reasons", "Reasons"),
    ]

    widths = {}
    for key, header in columns:
        cell_width = max((len(row[key]) for row in rows), default=0)
        widths[key] = max(len(header), cell_width)

    def format_row(row_dict: dict) -> str:
        return "| " + " | ".join(
            row_dict[key].ljust(widths[key]) for key, _ in columns
        ) + " |"

    separator = "+-" + "-+-".join("-" * widths[key] for key, _ in columns) + "-+"
    header_row = {key: header for key, header in columns}

    print(separator)
    print(format_row(header_row))
    print(separator)
    for row in rows:
        print(format_row(row))
    print(separator)


def print_recommendations_for_profile(profile_name: str, user_prefs: dict, songs: list) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\n=== {profile_name} ===")
    print(f"Preferences: {user_prefs}\n")
    _print_recommendations_table(recommendations)


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
