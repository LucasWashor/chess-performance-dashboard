import requests
import pandas as pd

username = "Lucas_W569"

headers = {
    "User-Agent": "chess-performance-dashboard/1.0 (username: Lucas_W569)"
}

# Get archive URLs
archives_url = f"https://api.chess.com/pub/player/{username}/games/archives"

response = requests.get(archives_url, headers=headers)

if response.status_code != 200:
    print("Error getting archives.")
    print("Status code:", response.status_code)
    print(response.text)
    exit()

archives = response.json()["archives"]

games_data = []

# Loop through all monthly archives
for archive_url in archives:

    games_response = requests.get(archive_url, headers=headers)

    if games_response.status_code != 200:
        print(f"Skipping archive due to error: {archive_url}")
        continue

    games = games_response.json()["games"]

    for game in games:

        white = game["white"]
        black = game["black"]

        # Determine whether user played white or black
        if white["username"].lower() == username.lower():

            color = "white"
            user_rating = white.get("rating")
            opponent_rating = black.get("rating")
            opponent = black["username"]
            result = white["result"]

        else:

            color = "black"
            user_rating = black.get("rating")
            opponent_rating = white.get("rating")
            opponent = white["username"]
            result = black["result"]

        games_data.append({
            "end_time": game.get("end_time"),
            "url": game.get("url"),
            "time_control": game.get("time_control"),
            "rated": game.get("rated"),
            "rules": game.get("rules"),
            "color": color,
            "opponent": opponent,
            "user_rating": user_rating,
            "opponent_rating": opponent_rating,
            "rating_diff": (
                user_rating - opponent_rating
                if user_rating and opponent_rating
                else None
            ),
            "result": result,
            "eco_url": game.get("eco"),
            "pgn": game.get("pgn")
        })

# Create dataframe
df = pd.DataFrame(games_data)

# Save CSV
df.to_csv("data/chess_games.csv", index=False)

print("CSV saved to data/chess_games.csv")
print(f"Total games downloaded: {len(df)}")
print(df.head())