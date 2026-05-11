import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Create outputs folder if it doesn't exist
Path("outputs").mkdir(exist_ok=True)

# Load cleaned data
df = pd.read_csv("data/chess_games_cleaned.csv")
df["end_time"] = pd.to_datetime(df["end_time"])

# ----------------------------
# Chart 1: Rating over time by time control
# ----------------------------
for control, label in {
    "60": "Bullet 1 Minute",
    "180": "Blitz 3 Minute",
    "600": "Rapid 10 Minute"
}.items():

    filtered = df[df["time_control"] == control].sort_values("end_time")

    if len(filtered) == 0:
        continue

    plt.figure(figsize=(12, 6))
    plt.plot(filtered["end_time"], filtered["user_rating"])
    plt.title(f"Rating Over Time: {label}")
    plt.xlabel("Date")
    plt.ylabel("Rating")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"outputs/rating_over_time_{control}.png")
    plt.close()

# ----------------------------
# Chart 2: Win rate by hour
# ----------------------------
hour_stats = df.groupby("hour").agg(
    games=("hour", "count"),
    win_rate=("simple_result", lambda x: (x == "win").mean() * 100)
).reset_index()

plt.figure(figsize=(10, 6))
plt.plot(hour_stats["hour"], hour_stats["win_rate"], marker="o")
plt.title("Win Rate by Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Win Rate (%)")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/win_rate_by_hour.png")
plt.close()

# ----------------------------
# Chart 3: Top openings by games played
# ----------------------------
top_openings = df["opening"].value_counts().head(10)

plt.figure(figsize=(12, 7))
top_openings.sort_values().plot(kind="barh")
plt.title("Top 10 Most Played Openings")
plt.xlabel("Number of Games")
plt.ylabel("Opening")
plt.tight_layout()
plt.savefig("outputs/top_openings.png")
plt.close()

# ----------------------------
# Chart 4: Best openings by win rate
# Minimum 30 games to avoid tiny sample sizes
# ----------------------------
opening_stats = df.groupby("opening").agg(
    games=("opening", "count"),
    win_rate=("simple_result", lambda x: (x == "win").mean() * 100)
).reset_index()

opening_stats = opening_stats[opening_stats["games"] >= 30]
opening_stats = opening_stats.sort_values("win_rate", ascending=False).head(10)

plt.figure(figsize=(12, 7))
plt.barh(opening_stats["opening"], opening_stats["win_rate"])
plt.title("Best Openings by Win Rate, Minimum 30 Games")
plt.xlabel("Win Rate (%)")
plt.ylabel("Opening")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("outputs/best_openings.png")
plt.close()

print("Charts saved in the outputs folder.")