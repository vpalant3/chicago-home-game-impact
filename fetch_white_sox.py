from pathlib import Path
from pybaseball import schedule_and_record

data_folder = Path("data")
data_folder.mkdir(exist_ok=True)

print("Starting White Sox data download...")
white_sox = schedule_and_record(2025, "CHW")

output_file = data_folder / "white_sox_2025_raw.csv"
white_sox.to_csv(output_file, index=False)

print(white_sox.head())
print(f"\nDownloaded {len(white_sox)} games.")
print(f"Saved data to: {output_file}")
