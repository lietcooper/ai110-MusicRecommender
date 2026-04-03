"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# Standard user profiles
# ---------------------------------------------------------------------------

HIGH_ENERGY_HIP_HOP = {
    "mood":         "energetic",
    "genre":        "hip-hop",
    "energy":       0.85,
    "acousticness": 0.10,
    "danceability": 0.88,
    "valence":      0.70,
}

CHILL_LOFI = {
    "mood":         "focused",
    "genre":        "lofi",
    "energy":       0.35,
    "acousticness": 0.80,
    "danceability": 0.55,
    "valence":      0.55,
}

DEEP_INTENSE_ROCK = {
    "mood":         "intense",
    "genre":        "rock",
    "energy":       0.90,
    "acousticness": 0.05,
    "danceability": 0.50,
    "valence":      0.30,
}

# ---------------------------------------------------------------------------
# Adversarial / edge-case profiles
# ---------------------------------------------------------------------------

# Conflict: high energy (0.9) paired with a sad mood.
# Expected tension: numeric energy score will boost upbeat, danceable songs,
# but those rarely carry a "sad" mood label — so mood points go to low-energy
# tracks and numeric points go to the opposite. Watch for mixed, mediocre
# scores across the board with no clear winner.
HIGH_ENERGY_SAD = {
    "mood":         "sad",
    "genre":        "blues",
    "energy":       0.90,
    "acousticness": 0.50,
    "danceability": 0.50,
    "valence":      0.10,
}

# Conflict: perfectly neutral numeric preferences (all 0.5).
# The only differentiator is the categorical match, so genre/mood dominate
# the ranking. Exposes how heavily the system relies on exact label matches.
ALL_MIDDLE = {
    "mood":         "happy",
    "genre":        "pop",
    "energy":       0.50,
    "acousticness": 0.50,
    "danceability": 0.50,
    "valence":      0.50,
}

# Conflict: genre that doesn't exist in the catalog ("jazz").
# No song earns the +1.5 genre bonus, so the full ranking falls back to
# mood and numeric proximity. Tests graceful degradation when preferences
# don't match any catalog entry.
MISSING_GENRE = {
    "mood":         "peaceful",
    "genre":        "jazz",       # not in songs.csv
    "energy":       0.25,
    "acousticness": 0.90,
    "danceability": 0.30,
    "valence":      0.65,
}


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

PROFILES = [
    ("High-Energy Hip-Hop",  HIGH_ENERGY_HIP_HOP),
    ("Chill Lofi",           CHILL_LOFI),
    ("Deep Intense Rock",    DEEP_INTENSE_ROCK),
    ("High-Energy Sad [adversarial]",  HIGH_ENERGY_SAD),
    ("All-Middle Neutral [adversarial]", ALL_MIDDLE),
    ("Missing Genre [adversarial]",    MISSING_GENRE),
]


def main() -> None:
    songs = load_songs("data/songs.csv")

    for label, user_prefs in PROFILES:
        print(f"\n{'='*60}")
        print(f"Profile: {label}")
        print(f"{'='*60}")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        for song, score, explanation in recommendations:
            print(f"  {song['title']} — Score: {score:.2f}")
            print(f"    Because: {explanation}")


if __name__ == "__main__":
    main()
