from pathlib import Path
import pandas as pd

input_file = Path("data/white_sox_2025_raw.csv")
output_file = Path("data/white_sox_2025_clean.csv")

games = pd.read_csv(input_file)

date_parts = games["Date"].str.extract(r"([A-Za-z]{3})\s+(\d{1,2})")
games["Game_Date"] = pd.to_datetime(
    date_parts[0] + " " + date_parts[1] + " 2025",
    format="%b %d %Y"
)

games["Is_Win"] = games["W/L"].astype(str).str.startswith("W").astype(int)
games["Recent_Win_Pct"] = (
    games["Is_Win"]
    .shift(1)
    .rolling(5, min_periods=1)
    .mean()
)
games["Run_Differential"] = games["R"] - games["RA"]

home_games = games[games["Home_Away"] == "Home"].copy()

home_games["Day_of_Week"] = home_games["Game_Date"].dt.day_name()
home_games["Attendance_Index"] = (
    home_games["Attendance"] / home_games["Attendance"].mean()
)

home_games = home_games.rename(
    columns={
        "Tm": "Team",
        "Opp": "Opponent",
        "W/L": "Result",
        "R": "Score_For",
        "RA": "Score_Against"
    }
)
home_games["Result"] = home_games["Result"].replace({
    "W": "Win",
    "L": "Loss",
    "W-wo": "Walk-off Win",
    "L-wo": "Walk-off Loss"
})


columns_to_keep = [
    "Game_Date",
    "Team",
    "Opponent",
    "Result",
    "Score_For",
    "Score_Against",
    "Attendance",
    "Is_Win",
    "Recent_Win_Pct",
    "Run_Differential",
    "Day_of_Week",
    "Attendance_Index"
]

home_games[columns_to_keep].to_csv(output_file, index=False)

print(f"Cleaned {len(home_games)} home games.")
print(f"Average home attendance: {home_games['Attendance'].mean():,.0f}")
print(f"Saved clean data to: {output_file}")
