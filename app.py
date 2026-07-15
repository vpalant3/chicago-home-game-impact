from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Chicago Home-Game Impact",
    page_icon="🏟️",
    layout="wide"
)

base_folder = Path(__file__).parent

teams = {
    "Chicago White Sox": {
        "file": "white_sox_2025_clean.csv",
        "season": "2025",
        "short_name": "White Sox"
    },
    "Chicago Bulls": {
        "file": "bulls_2025_26_clean.csv",
        "season": "2025–26",
        "short_name": "Bulls"
    },
    "Chicago Fire FC": {
        "file": "fire_2025_clean.csv",
        "season": "2025",
        "short_name": "Fire"
    }
}


@st.cache_data
def load_data(file_name):
    data_file = base_folder / "data" / file_name
    return pd.read_csv(data_file, parse_dates=["Game_Date"])


def relationship_strength(value):
    absolute_value = abs(value)

    if absolute_value < 0.20:
        return "very weak"
    if absolute_value < 0.40:
        return "weak"
    if absolute_value < 0.60:
        return "moderate"
    return "strong"


st.title("Chicago Home-Game Impact")

st.write(
    "**Core question:** Across Chicago professional sports teams, "
    "which factors are most strongly associated with home-game attendance: "
    "recent performance, game timing, or opponent appeal?"
)

selected_team = st.selectbox(
    "Select a team",
    list(teams.keys())
)

team = teams[selected_team]
games = load_data(team["file"])

st.subheader(
    f"{selected_team} — {team['season']} Home Attendance"
)

st.write(
    f"This dashboard explores how recent team performance, scheduling, "
    f"and opponent appeal relate to attendance at {team['short_name']} "
    f"home games."
)

average_attendance = games["Attendance"].mean()
home_win_rate = games["Is_Win"].mean()

column1, column2, column3 = st.columns(3)

column1.metric("Home Games", len(games))
column2.metric(
    "Average Attendance",
    f"{average_attendance:,.0f}"
)
column3.metric(
    "Home Win Rate",
    f"{home_win_rate:.1%}"
)

st.subheader("Attendance Over Time")

attendance_chart = px.line(
    games.sort_values("Game_Date"),
    x="Game_Date",
    y="Attendance",
    markers=True,
    hover_data=["Opponent", "Result"],
    labels={
        "Game_Date": "Game Date",
        "Attendance": "Attendance"
    }
)

st.plotly_chart(attendance_chart, width="stretch")

analysis_games = games.dropna(
    subset=["Recent_Win_Pct"]
)

correlation = analysis_games["Recent_Win_Pct"].corr(
    analysis_games["Attendance"]
)

weekend_days = ["Friday", "Saturday", "Sunday"]

weekend_average = games.loc[
    games["Day_of_Week"].isin(weekend_days),
    "Attendance"
].mean()

weekday_average = games.loc[
    ~games["Day_of_Week"].isin(weekend_days),
    "Attendance"
].mean()

weekend_lift = weekend_average / weekday_average - 1

opponent_summary = (
    games.groupby("Opponent", as_index=False)
    .agg(
        Average_Attendance=("Attendance", "mean"),
        Games=("Attendance", "size")
    )
)

repeat_opponents = opponent_summary.loc[
    opponent_summary["Games"] >= 2
]

if repeat_opponents.empty:
    ranked_opponents = opponent_summary
    opponent_scope = "Across all home opponents"
else:
    ranked_opponents = repeat_opponents
    opponent_scope = "Among opponents with multiple home games"

top_opponent = ranked_opponents.sort_values(
    "Average_Attendance",
    ascending=False
).iloc[0]

top_opponent_name = top_opponent["Opponent"]
top_opponent_average = top_opponent["Average_Attendance"]
top_opponent_games = int(top_opponent["Games"])

opponent_lift = (
    top_opponent_average / average_attendance - 1
)

st.subheader("What Appears to Drive Attendance?")

left_chart, right_chart = st.columns(2)

with left_chart:
    performance_chart = px.scatter(
        analysis_games,
        x="Recent_Win_Pct",
        y="Attendance",
        color="Result",
        hover_data=["Game_Date", "Opponent"],
        labels={
            "Recent_Win_Pct": "Prior 5-Game Win Rate",
            "Attendance": "Attendance"
        },
        title="Recent Performance vs. Attendance"
    )

    performance_chart.update_xaxes(
        tickformat=".0%"
    )

    st.plotly_chart(
        performance_chart,
        width="stretch"
    )

with right_chart:
    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    day_summary = (
        games.groupby(
            "Day_of_Week",
            as_index=False
        )["Attendance"].mean()
    )

    day_summary["Day_of_Week"] = pd.Categorical(
        day_summary["Day_of_Week"],
        categories=day_order,
        ordered=True
    )

    day_summary = day_summary.sort_values(
        "Day_of_Week"
    )

    day_chart = px.bar(
        day_summary,
        x="Day_of_Week",
        y="Attendance",
        labels={
            "Day_of_Week": "Day",
            "Attendance": "Average Attendance"
        },
        title="Average Attendance by Day",
        text_auto=",.0f"
    )

    st.plotly_chart(
        day_chart,
        width="stretch"
    )

correlation_direction = (
    "positive" if correlation >= 0 else "negative"
)

weekend_direction = (
    "higher" if weekend_lift >= 0 else "lower"
)

opponent_direction = (
    "above" if opponent_lift >= 0 else "below"
)

st.subheader(
    f"{team['short_name']} Preliminary Finding"
)

st.info(
    f"Recent performance had a "
    f"{relationship_strength(correlation)} "
    f"{correlation_direction} relationship with attendance "
    f"(correlation: {correlation:.2f}). Friday–Sunday games "
    f"averaged {weekend_average:,.0f} attendees, compared with "
    f"{weekday_average:,.0f} for Monday–Thursday games—"
    f"{abs(weekend_lift):.0%} {weekend_direction}. {opponent_scope}, "
    f"{top_opponent_name} produced the "
    f"highest average attendance at {top_opponent_average:,.0f} "
    f"across {top_opponent_games} games, "
    f"{abs(opponent_lift):.0%} {opponent_direction} the overall "
    f"average. These relationships show association, not causation."
)

st.divider()

st.subheader("Across-Team Executive Summary")

summary1, summary2, summary3 = st.columns(3)

summary1.metric(
    "Strongest Performance Relationship",
    "Chicago Fire: 0.20"
)

summary2.metric(
    "Largest Weekend Attendance Lift",
    "White Sox: +79%"
)

summary3.metric(
    "Largest Opponent Attendance Spike",
    "Fire vs. Miami: +166%"
)

st.success(
    "**Overall finding:** Opponent appeal and game timing appear "
    "more strongly associated with attendance than recent team "
    "performance. Cubs games more than doubled normal White Sox "
    "attendance, while the Fire match against Miami attracted "
    "166% more fans than the Fire's average home game. Meanwhile, "
    "the relationship between recent winning and attendance remained "
    "weak for all three teams. For sports organizations, this supports "
    "premium marketing around rivalry and star-opponent games, combined "
    "with targeted promotions for lower-demand weekday games."
)

st.caption(
    "These findings describe associations, not causation. The Fire's "
    "weekend comparison is based on only one weekday home match. "
    "Attendance percentages are compared within each team because "
    "venue capacity, league schedules, and season lengths differ."
)

st.subheader("Game Data")

display_columns = [
    "Game_Date",
    "Opponent",
    "Result",
    "Score_For",
    "Score_Against",
    "Attendance",
    "Recent_Win_Pct"
]

st.dataframe(
    games[display_columns],
    hide_index=True,
    width="stretch",
    column_config={
        "Game_Date": st.column_config.DateColumn(
            "Game Date",
            format="MMM D, YYYY"
        ),
        "Score_For": st.column_config.NumberColumn(
            f"{team['short_name']} Score",
            format="%d"
        ),
        "Score_Against": st.column_config.NumberColumn(
            "Opponent Score",
            format="%d"
        ),
        "Attendance": st.column_config.NumberColumn(
            "Attendance",
            format="%d"
        ),
        "Recent_Win_Pct": st.column_config.NumberColumn(
            "Prior 5-Game Win Rate",
            format="percent"
        )
    }
)
