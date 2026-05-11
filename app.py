import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Chess Performance Dashboard", layout="wide")

st.title("Chess.com Personal Performance Dashboard")
st.write("Analysis of Lucas_W569's Chess.com game history.")

df = pd.read_csv("data/chess_games_cleaned.csv")
df["end_time"] = pd.to_datetime(df["end_time"])

# Sidebar filters
st.sidebar.header("Filters")

time_controls = {
    "Bullet 1 Minute": "60",
    "Blitz 3 Minute": "180",
    "Rapid 10 Minute": "600"
}

selected_label = st.sidebar.selectbox(
    "Time Control",
    list(time_controls.keys())
)

selected_control = time_controls[selected_label]

filtered = df[df["time_control"] == selected_control].copy()
filtered = filtered.sort_values("end_time")

# Key metrics
col1, col2, col3, col4 = st.columns(4)

total_games = len(filtered)
win_rate = (filtered["simple_result"] == "win").mean() * 100
avg_rating = filtered["user_rating"].mean()
peak_rating = filtered["user_rating"].max()

col1.metric("Total Games", f"{total_games:,}")
col2.metric("Win Rate", f"{win_rate:.1f}%")
col3.metric("Average Rating", f"{avg_rating:.0f}")
col4.metric("Peak Rating", f"{peak_rating:.0f}")

# Rating over time
st.subheader(f"Rating Over Time: {selected_label}")

fig_rating = px.line(
    filtered,
    x="end_time",
    y="user_rating",
    title=f"Rating Over Time ({selected_label})"
)

st.plotly_chart(fig_rating, use_container_width=True)

# Win rate by hour
st.subheader("Win Rate by Hour of Day")

hour_stats = filtered.groupby("hour").agg(
    games=("hour", "count"),
    win_rate=("simple_result", lambda x: (x == "win").mean() * 100)
).reset_index()

fig_hour = px.line(
    hour_stats,
    x="hour",
    y="win_rate",
    markers=True,
    hover_data=["games"],
    title="Win Rate by Hour"
)

st.plotly_chart(fig_hour, use_container_width=True)

# Top openings
st.subheader("Most Played Openings")

top_openings = (
    filtered["opening"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_openings.columns = ["opening", "games"]

fig_openings = px.bar(
    top_openings,
    x="games",
    y="opening",
    orientation="h",
    title="Top 10 Most Played Openings"
)

st.plotly_chart(fig_openings, use_container_width=True)

# Best openings
st.subheader("Best Openings by Win Rate")

opening_stats = filtered.groupby("opening").agg(
    games=("opening", "count"),
    win_rate=("simple_result", lambda x: (x == "win").mean() * 100)
).reset_index()

opening_stats = opening_stats[opening_stats["games"] >= 10]
opening_stats = opening_stats.sort_values("win_rate", ascending=False).head(10)

fig_best = px.bar(
    opening_stats,
    x="win_rate",
    y="opening",
    orientation="h",
    hover_data=["games"],
    title="Best Openings by Win Rate, Minimum 10 Games"
)

st.plotly_chart(fig_best, use_container_width=True)