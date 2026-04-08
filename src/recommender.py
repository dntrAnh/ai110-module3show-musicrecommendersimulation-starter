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
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into typed dictionaries."""
    songs: List[Dict] = []

    with open(csv_path, "r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                    "popularity": int(row["popularity"]),
                    "release_decade": int(row["release_decade"]),
                    "mood_tag": row["mood_tag"],
                    "instrumentalness": float(row["instrumentalness"]),
                    "lyrical_density": float(row["lyrical_density"]),
                    "live_energy": float(row["live_energy"]),
                }
            )

    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Compute a recommendation score and human-readable reasons for one song."""
    score = 0.0
    reasons: List[str] = []

    user_genre = str(user_prefs.get("genre", "")).strip().lower()
    song_genre = str(song.get("genre", "")).strip().lower()
    if user_genre and song_genre and user_genre == song_genre:
        score += 1.0
        reasons.append("genre match (+1.0)")

    user_mood = str(user_prefs.get("mood", "")).strip().lower()
    song_mood = str(song.get("mood", "")).strip().lower()
    if user_mood and song_mood and user_mood == song_mood:
        score += 1.0
        reasons.append("mood match (+1.0)")

    if "energy" in user_prefs and "energy" in song:
        energy_diff = abs(float(song["energy"]) - float(user_prefs["energy"]))
        energy_score = max(0.0, 3.0 - 6.0 * energy_diff)
        if energy_score > 0:
            score += energy_score
            reasons.append(f"energy similarity (+{energy_score:.2f})")

    if "popularity_target" in user_prefs and "popularity" in song:
        popularity_diff = abs(int(song["popularity"]) - int(user_prefs["popularity_target"]))
        popularity_score = max(0.0, 1.2 - 0.02 * popularity_diff)
        if popularity_score > 0:
            score += popularity_score
            reasons.append(f"popularity proximity (+{popularity_score:.2f})")

    if "preferred_decade" in user_prefs and "release_decade" in song:
        if int(song["release_decade"]) == int(user_prefs["preferred_decade"]):
            score += 0.8
            reasons.append("preferred decade match (+0.8)")

    user_mood_tag = str(user_prefs.get("mood_tag", "")).strip().lower()
    song_mood_tag = str(song.get("mood_tag", "")).strip().lower()
    if user_mood_tag and song_mood_tag and user_mood_tag == song_mood_tag:
        score += 0.9
        reasons.append("mood tag match (+0.9)")

    if "instrumentalness_target" in user_prefs and "instrumentalness" in song:
        inst_diff = abs(float(song["instrumentalness"]) - float(user_prefs["instrumentalness_target"]))
        inst_score = max(0.0, 1.0 - 2.5 * inst_diff)
        if inst_score > 0:
            score += inst_score
            reasons.append(f"instrumentalness proximity (+{inst_score:.2f})")

    if "lyrical_density_target" in user_prefs and "lyrical_density" in song:
        lyric_diff = abs(float(song["lyrical_density"]) - float(user_prefs["lyrical_density_target"]))
        lyric_score = max(0.0, 0.8 - 2.0 * lyric_diff)
        if lyric_score > 0:
            score += lyric_score
            reasons.append(f"lyrical density proximity (+{lyric_score:.2f})")

    if "live_energy_target" in user_prefs and "live_energy" in song:
        live_diff = abs(float(song["live_energy"]) - float(user_prefs["live_energy_target"]))
        live_score = max(0.0, 0.8 - 2.0 * live_diff)
        if live_score > 0:
            score += live_score
            reasons.append(f"live energy proximity (+{live_score:.2f})")

    if not reasons:
        reasons.append("no direct genre/mood/energy matches")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank songs by score, then apply diversity penalties during top-k selection."""
    if k <= 0:
        return []

    # Diversity penalty weights used during greedy top-k construction.
    artist_repeat_penalty = 0.60
    genre_repeat_penalty = 0.30

    candidates: List[Dict] = []
    for song in songs:
        base_score, reasons = score_song(user_prefs, song)
        candidates.append(
            {
                "song": song,
                "base_score": base_score,
                "reasons": reasons,
            }
        )

    selected: List[Tuple[Dict, float, str]] = []
    selected_artist_counts: Dict[str, int] = {}
    selected_genre_counts: Dict[str, int] = {}

    while candidates and len(selected) < k:
        best_idx = 0
        best_adjusted = float("-inf")
        best_artist_penalty = 0.0
        best_genre_penalty = 0.0

        for idx, candidate in enumerate(candidates):
            song = candidate["song"]
            artist = str(song.get("artist", "")).strip().lower()
            genre = str(song.get("genre", "")).strip().lower()

            artist_penalty = artist_repeat_penalty * selected_artist_counts.get(artist, 0)
            genre_penalty = genre_repeat_penalty * selected_genre_counts.get(genre, 0)
            adjusted_score = candidate["base_score"] - artist_penalty - genre_penalty

            if adjusted_score > best_adjusted:
                best_idx = idx
                best_adjusted = adjusted_score
                best_artist_penalty = artist_penalty
                best_genre_penalty = genre_penalty

        chosen = candidates.pop(best_idx)
        chosen_song = chosen["song"]
        chosen_reasons = list(chosen["reasons"])

        if best_artist_penalty > 0:
            chosen_reasons.append(f"diversity penalty artist repeat (-{best_artist_penalty:.2f})")
        if best_genre_penalty > 0:
            chosen_reasons.append(f"diversity penalty genre repeat (-{best_genre_penalty:.2f})")

        explanation = ", ".join(chosen_reasons)
        selected.append((chosen_song, best_adjusted, explanation))

        artist_key = str(chosen_song.get("artist", "")).strip().lower()
        genre_key = str(chosen_song.get("genre", "")).strip().lower()
        selected_artist_counts[artist_key] = selected_artist_counts.get(artist_key, 0) + 1
        selected_genre_counts[genre_key] = selected_genre_counts.get(genre_key, 0) + 1

    return selected
