from io import StringIO
from pathlib import Path

import pandas as pd
import requests

data_folder = Path("data")
data_folder.mkdir(exist_ok=True)

url = "https://www.basketball-reference.com/teams/CHI/2026_games.html"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
    )
}

print("Starting Bulls data download...")

response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()

tables = pd.read_html(StringIO(response.text))

bulls = next(
    table
    for table in tables
    if {"Date","Opponent", "Attend."}.issubset(table.columns)
)

bulls = bulls[bulls["Date"] != "Date"].copy()

output_file = data_folder / "bulls_2025_26_raw.csv"
bulls.to_csv(output_file, index=False)

print(bulls.head())
print(f"\nDownloaded {len(bulls)} Bulls games.")
print("Columns:", bulls.columns.tolist())
print(f"Saved raw data to: {output_file}")
