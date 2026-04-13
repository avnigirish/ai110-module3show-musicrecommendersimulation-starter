"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    # Taste profile: a focused late-night indie listener
    # - Prefers indie pop with a moody emotional tone
    # - Moderate-to-high energy (alert but not intense)
    # - Not acoustic-leaning — comfortable with produced, electronic textures
    # - valence kept low-mid to allow moody/bittersweet songs through
    user_prefs = {
        "genre":         "indie pop",
        "mood":          "moody",
        "target_energy": 0.72,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"User profile: genre={user_prefs['genre']!r}, mood={user_prefs['mood']!r}, "
          f"energy={user_prefs['target_energy']}, acoustic={user_prefs['likes_acoustic']}")
    print()
    print("=" * 52)
    print(f"  Top {len(recommendations)} Recommendations")
    print("=" * 52)
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"\n  #{i}  {song['title']} — {song['artist']}")
        print(f"       Score : {score:.2f} / 4.50")
        print(f"       Why   : {explanation}")


if __name__ == "__main__":
    main()
