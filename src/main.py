"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profile: target values for each scoring feature.
    # Numeric values are on a 0.0–1.0 scale matching the CSV columns.
    user_prefs = {
        "mood":         "energetic",  # primary listening intent
        "genre":        "hip-hop",    # preferred style
        "energy":       0.85,         # high intensity
        "acousticness": 0.10,         # electronic / produced sound
        "danceability": 0.88,         # strong groove preference
        "valence":      0.70,         # generally positive feel
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
