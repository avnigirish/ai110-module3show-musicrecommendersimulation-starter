"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def print_recommendations(label, user_prefs, songs, k=5):
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print(f"\nProfile: {label}")
    print(f"  genre={user_prefs['genre']!r}, mood={user_prefs['mood']!r}, "
          f"energy={user_prefs['target_energy']}, acoustic={user_prefs['likes_acoustic']}")
    print("=" * 52)
    print(f"  Top {len(recommendations)} Recommendations")
    print("=" * 52)
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"\n  #{i}  {song['title']} — {song['artist']}")
        print(f"       Score : {score:.2f} / 4.50")
        print(f"       Why   : {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # --- Standard profiles ---

    # 1. High-Energy Pop — gym / workout listener
    print_recommendations("High-Energy Pop", {
        "genre":          "pop",
        "mood":           "intense",
        "target_energy":  0.92,
        "likes_acoustic": False,
    }, songs)

    # 2. Chill Lofi — studying / background focus
    print_recommendations("Chill Lofi", {
        "genre":          "lofi",
        "mood":           "chill",
        "target_energy":  0.38,
        "likes_acoustic": True,
    }, songs)

    # 3. Deep Intense Rock — high energy, raw texture
    print_recommendations("Deep Intense Rock", {
        "genre":          "rock",
        "mood":           "intense",
        "target_energy":  0.90,
        "likes_acoustic": False,
    }, songs)

    # --- Adversarial / edge-case profiles ---

    # 4. Conflict: high energy but sad mood — workout but melancholic
    #    Tests whether energy or mood wins when they point to different songs
    print_recommendations("EDGE: High Energy + Sad Mood", {
        "genre":          "soul",
        "mood":           "sad",
        "target_energy":  0.90,
        "likes_acoustic": False,
    }, songs)

    # 5. Genre that doesn't exist in catalog — no genre points ever fire
    #    Tests score when genre match is always 0
    print_recommendations("EDGE: Unknown Genre", {
        "genre":          "bossa nova",
        "mood":           "relaxed",
        "target_energy":  0.40,
        "likes_acoustic": True,
    }, songs)

    # 6. Extreme acoustic preference vs zero-acoustic catalog entries
    #    likes_acoustic=True targets 0.8; all electronic songs score low on acousticness
    print_recommendations("EDGE: Max Acoustic Preference", {
        "genre":          "classical",
        "mood":           "melancholic",
        "target_energy":  0.21,
        "likes_acoustic": True,
    }, songs)


if __name__ == "__main__":
    main()
