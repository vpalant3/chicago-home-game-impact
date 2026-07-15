from pathlib import Path

import pandas as pd

input_file = Path("data/bulls_2025_26_raw.csv")
output_file = Path("data/bulls_2025_26_clean.csv")

games = pd.read_csv(input_file)

games["Game_Date"] = pd.to_datetime(
    games["Date"],
    format="%a, %b %d, %Y"
)

games["Is_Win"] = (
    games["Unnamed: 7"] == "W"
).astype(int)

games["Recent_Win_Pct"] = (
    games["Is_Win"]
    .shift(1)
    .rolling(5, min_periods=1)
    .mean()
)

games["Score_Differential"] = games["Tm"] - games["Opp"]

home_games = games[games["Unnamed: 5"].isna()].copy()

home_games = home_games.rename(
    columns={
        "Unnamed: 7": "Result",
        "Tm": "Score_For",
        "Opp": "Score_Against",
        "Attend.": "Attendance"
    }
)

home_games["Result"] = home_games["Result"].replace(
    {
        "W":"Win",
        "L": "Loss"
    }
)

home_games["Team"] = "CHI"
home_games["Team_Name"] = "Chicago Bulls"
home_games["League"] = "NBA"
home_games["Season"] = "2025-26"
home_games["Day_of_Week"] = home_games["Game_Date"].dt.day_name()

home_games["Attendance_Index"] = (
    home_games["Attendance"] /
    home_games["Attendance"].mean()
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
    "Attendance_Index"
]

home_games[columns_to_keep].to_csv(output_file, index=False)

print(home_games[columns_to_keep].head())
print(f"\nCleaned {len(home_games)} Bulls home games.")
print(f"Total attendance: {home_games['Attendance'].sum():,.0f}")
print(f"Average attendance: {home_games['Attendance'].mean():,.0f}")
print(f"Saved clean data to: {output_file}")
