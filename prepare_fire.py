from pathlib import Path

import pandas as pd

input_file = Path("data/fire_2025_raw.csv")
output_file = Path("data/fire_2025_clean.csv")

games = pd.read_csv(input_file)

games["Game_Date"] = pd.to_datetime(games["Game_Date"])
games = games.sort_values("Game_Date").reset_index(drop=True)

games["HomeTeamScore"] = pd.to_numeric(games["HomeTeamScore"])
games["AwayTeamScore"] = pd.to_numeric(games["AwayTeamScore"])

# Put every result from Chicago's perspective
games["Opponent"] = games["AwayTeam"].where(
    games["Is_Home"],
    games["HomeTeam"]
)

games["Score_For"] = games["HomeTeamScore"].where(
    games["Is_Home"],
    games["AwayTeamScore"]
)

games["Score_Against"] = games["AwayTeamScore"].where(
    games["Is_Home"],
    games["HomeTeamScore"]
)

games["Result"] = "Draw"

games.loc[
    games["Score_For"] > games["Score_Against"],
    "Result"
] = "Win"

games.loc[
    games["Score_For"] < games["Score_Against"],
    "Result"
] = "Loss"

games["Is_Win"] = (games["Result"] == "Win").astype(int)

# Winning percentage in the five matches before each game
games["Recent_Win_Pct"] = (
    games["Is_Win"]
    .shift(1)
    .rolling(5, min_periods=1)
    .mean()
)

# Keep only Fire home matches
home_games = games.loc[games["Is_Home"]].copy()

home_games["Team"] = "CHI"
home_games["Team_Name"] = "Chicago Fire FC"
home_games["League"] = "MLS"
home_games["Season"] = "2025"
home_games["Day_of_Week"] = home_games["Game_Date"].dt.day_name()

home_games["Attendance"] = pd.to_numeric(
    home_games["Attendance"]
).astype(int)

home_games["Score_For"] = home_games["Score_For"].astype(int)
home_games["Score_Against"] = home_games["Score_Against"].astype(int)

home_games["Attendance_Index"] = (
    home_games["Attendance"]
    / home_games["Attendance"].mean()
)

home_games = home_games.rename(
    columns={"Location": "Venue"}
)

columns_to_keep = [
    "Game_Date",
    "Team",
    "Team_Name",
    "League",
    "Season",
    "Opponent",
    "Result",
    "Score_For",
    "Score_Against",
    "Attendance",
    "Is_Win",
    "Recent_Win_Pct",
    "Score_Differential",
    "Day_of_Week",
    "Attendance_Index",
    "Venue"
]

home_games["Score_Differential"] = (
    home_games["Score_For"]
    - home_games["Score_Against"]
)

home_games[columns_to_keep].to_csv(
    output_file,
    index=False
)

print(home_games[columns_to_keep].head())
print(f"\nCleaned {len(home_games)} Fire home games.")
print(
    f"Average attendance: "
    f"{home_games['Attendance'].mean():,.0f}"
)
print(
    f"Home win rate: "
    f"{home_games['Is_Win'].mean():.1%}"
)
print(f"Saved clean data to: {output_file}")
