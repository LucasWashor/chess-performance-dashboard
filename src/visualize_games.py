import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data/chess_games_cleaned.csv")
df = df[df["time_control"] == "180"]

# Convert datetime again just to be safe
df["end_time"] = pd.to_datetime(df["end_time"])

# Sort chronologically
df = df.sort_values("end_time")

# Plot rating over time
plt.figure(figsize=(12, 6))

plt.plot(df["end_time"], df["user_rating"])

plt.title("Chess Rating Over Time")
plt.xlabel("Date")
plt.ylabel("Rating")

plt.grid(True)

plt.show()