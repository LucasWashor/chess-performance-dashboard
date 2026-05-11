import pandas as pd

# Load cleaned data
df = pd.read_csv("data/chess_games_cleaned.csv")

# Basic stats
print("\nTOTAL GAMES:")
print(len(df))

print("\nWIN RATE:")
win_rate = (df["simple_result"] == "win").mean() * 100
print(f"{win_rate:.2f}%")

# White vs Black
print("\nWHITE VS BLACK PERFORMANCE:")
color_performance = df.groupby("color")["simple_result"] \
    .apply(lambda x: (x == "win").mean() * 100)

print(color_performance)

# Most played openings
print("\nTOP 10 MOST PLAYED OPENINGS:")
print(df["opening"].value_counts().head(10))

# Best openings (minimum 10 games)
opening_stats = df.groupby("opening").agg(
    games=("opening", "count"),
    win_rate=("simple_result", lambda x: (x == "win").mean() * 100)
)

opening_stats = opening_stats[opening_stats["games"] >= 10]

print("\nBEST OPENINGS (MIN 10 GAMES):")
print(opening_stats.sort_values("win_rate", ascending=False).head(10))

# Best hour of day
hour_stats = df.groupby("hour").agg(
    games=("hour", "count"),
    win_rate=("simple_result", lambda x: (x == "win").mean() * 100)
)

print("\nBEST HOURS TO PLAY:")
print(hour_stats.sort_values("win_rate", ascending=False).head(10))