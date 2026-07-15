from pathlib import Path

import pandas as pd
import requests

data_folder = Path("data")
data_folder.mkdir(exist_ok=True)

# Public 2025 MLS schedule and results feed
url = "https://fixturedownload.com/feed/json/mls-2025"

print("Starting Chicago Fire data download...")

response = requests.get(url, timeout=30)
response.raise_for_status()

matches = pd.DataFrame(response.json())

# Keep every Chicago Fire match
fire = matches.loc[
    (matches["HomeTeam"] == "Chicago")
    | (matches["AwayTeam"] == "Chicago")
].copy()

# Convert the UTC kickoff date to Chicago's local date
local_times = pd.to_datetime(
    fire["DateUtc"],
    utc=True
).dt.tz_convert("America/Chicago")

fire["Game_Date"] = local_times.dt.strftime("%Y-%m-%d")
fire["Is_Home"] = fire["HomeTeam"] == "Chicago"

# Attendance reported for each Fire home match
attendance_by_date = {
    "2025-03-01": 20372,
    "2025-03-29": 16278,
    "2025-04-13": 62358,
    "2025-04-19": 17732,
    "2025-05-03": 17876,
    "2025-05-10": 22741,
    "2025-06-14": 26942,
    "2025-06-25": 17231,
    "2025-06-28": 17837,
    "2025-07-12": 27631,
    "2025-07-26": 29273,
    "2025-08-09": 19831,
    "2025-08-16": 17485,
    "2025-09-06": 16947,
    "2025-09-13": 20636,
    "2025-09-27": 23321,
    "2025-10-04": 24653
}

fire["Attendance"] = fire["Game_Date"].map(attendance_by_date)

output_file = data_folder / "fire_2025_raw.csv"
fire.to_csv(output_file, index=False)

home_games = fire.loc[fire["Is_Home"]]

print(fire.head())
print(f"\nDownloaded {len(fire)} Chicago Fire matches.")
print(
    f"Found {home_games['Attendance'].notna().sum()} "
    "home attendance values."
)
print(f"Saved raw data to: {output_file}")
