# Chicago Home-Game Impact

An interactive sports-business dashboard examining which factors are most strongly associated with home-game attendance across the Chicago White Sox, Chicago Bulls, and Chicago Fire FC.

## Core question

Across Chicago professional sports teams, is home-game attendance more closely associated with recent performance, game timing, or opponent appeal?

## Key findings

- Recent winning had only a weak relationship with attendance for all three teams. The highest correlation was Chicago Fire FC at `+0.20`.
- White Sox Friday-through-Sunday games averaged 79% higher attendance than Monday-through-Thursday games.
- White Sox games against the Cubs averaged 38,410 attendees, 115% above the White Sox home-game average.
- The Fire match against Miami drew 62,358 attendees, 166% above the Fire home-game average.
- Bulls attendance was comparatively stable: its weekend lift was approximately 2%, and its highest repeat-opponent lift was approximately 6%.

The overall finding is that opponent appeal and scheduling were more strongly associated with demand than recent winning. These results describe associations, not causation.

## Dashboard features

- Team selector for the White Sox, Bulls, and Fire
- Home-game, average-attendance, and home-win-rate KPIs
- Attendance-over-time chart
- Recent five-game win rate versus attendance analysis
- Weekday and weekend attendance comparison
- Opponent-demand analysis
- Team-specific findings and an across-team executive summary
- Searchable game-level data table

## Methodology

Each team was converted into a shared game-level format containing the date, opponent, result, team score, opponent score, attendance, day of week, and recent win rate.

`Recent_Win_Pct` is the team's win percentage over the five games preceding each home game. Shifting the calculation by one game prevents the current result from being used to describe attendance that was determined before the game was played.

The dashboard uses Pearson correlation to summarize the direction and strength of the relationship between recent win rate and attendance. Weekend games are defined as Friday through Sunday. Opponent demand is measured relative to each team's own average attendance so teams with different venues and capacities can be compared more fairly.

## Data sources

- White Sox schedule, results, and attendance: [Baseball Reference](https://www.baseball-reference.com/teams/CHW/2025-schedule-scores.shtml), retrieved with [`pybaseball`](https://github.com/jldbc/pybaseball)
- Bulls schedule, results, and attendance: [Basketball Reference](https://www.basketball-reference.com/teams/CHI/2026_games.html)
- Fire schedule and results: [FixtureDownload 2025 MLS results](https://fixturedownload.com/results/mls-2025)
- Fire attendance: [Chicago Fire FC match reports](https://www.chicagofirefc.com/news/)

Raw and cleaned CSV files are included in `data/` so the dashboard can run without downloading data when it starts.

## Limitations

- The three leagues have different season lengths, venue capacities, schedules, and ticketing environments.
- The Fire played only one Monday-through-Thursday home match in the dataset, so its weekend comparison should be interpreted cautiously.
- Opponent appeal is descriptive and does not control for promotions, ticket prices, weather, holidays, or star-player availability.
- Announced match-level Fire attendance figures sum to 500 more than the club's published season aggregate. The analysis uses the individual match-report figures because game-level observations are required.
- Correlation does not establish that winning, scheduling, or an opponent caused attendance to change.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Then open `http://localhost:8501`.

## Project structure

```text
SportsAnalyst/
|-- app.py
|-- data/
|   |-- bulls_2025_26_clean.csv
|   |-- fire_2025_clean.csv
|   `-- white_sox_2025_clean.csv
|-- fetch_bulls.py
|-- fetch_fire.py
|-- fetch_white_sox.py
|-- prepare_bulls.py
|-- prepare_fire.py
|-- prepare_white_sox.py
`-- requirements.txt
```

## Author

Vladislav Palant  
Information Science major and Business minor at the University of Illinois Urbana-Champaign

- [LinkedIn](https://www.linkedin.com/in/vladislav-palant-b6b060325/)
- [GitHub](https://github.com/vpalant3)
- Email: vladislavpalant@gmail.com

