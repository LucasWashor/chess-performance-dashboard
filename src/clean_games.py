import pandas as pd

# Load dataset
df = pd.read_csv("data/chess_games.csv")

# Convert Unix timestamp to datetime
df["end_time"] = pd.to_datetime(df["end_time"], unit="s")

# Create useful time columns
df["date"] = df["end_time"].dt.date
df["year"] = df["end_time"].dt.year
df["month"] = df["end_time"].dt.month
df["hour"] = df["end_time"].dt.hour
df["weekday"] = df["end_time"].dt.day_name()

# Simplify results
result_map = {
    "win": "win",
    "checkmated": "loss",
    "resigned": "loss",
    "timeout": "loss",
    "lose": "loss",
    "agreed": "draw",
    "repetition": "draw",
    "stalemate": "draw",
    "timevsinsufficient": "draw",
    "insufficient": "draw",
    "50move": "draw"
}

df["simple_result"] = df["result"].map(result_map)

# Extract opening name from ECO URL
df["opening"] = df["eco_url"].str.split("/").str[-1]
df["opening"] = df["opening"].str.replace("-", " ")

# Save cleaned dataset
df.to_csv("data/chess_games_cleaned.csv", index=False)

print("Cleaned dataset saved!")
print(df.head())