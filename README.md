# NBA Game Data Web Scraper

This repository contains a Python-based web scraper used to collect NBA game data from Basketball-Reference.  
The data is intended for sports analytics and machine learning projects, such as predicting game outcomes or building team performance models.

---

## What this project does

- Scrapes NBA regular season game results  
- Covers the last **5 NBA seasons**  
- Handles Basketball-Reference quirks like:
  - Cloudflare protection  
  - Commented HTML tables  
  - Different table layouts across months  
- Outputs a clean **CSV dataset** ready for analysis or ML models  

---

## Project structure
web-scraper/  
│  
├── nba_scraper.py # Final scraper (recommended entry point)  
├── extract_games.py # Controlled single-month extraction (debugging)  
├── find_table.py # Table detection and inspection  
├── request_test.py # Connection and access testing  
│  
├── data/  
│ └── nba_games_last_5_years.csv  
│  
├── README.md  
└── LICENSE  
---

## Requirements

- Python 3.10+

### Required Libraries

pip install pandas beautifulsoup4 cloudscraper

## How to Run the Scraper

Run the final scraper script:

python nba_scraper.py
this will
- Scrape all valid months for each season
- Skip months with no games
- Save the final dataset to: data/nba_games_last_5_years.csv

---

### Output Data Format

Each row represents one NBA game.

## Columns

- date – Game date

- away_team – Visiting team

- away_pts – Away team score

- home_team – Home team

- home_pts – Home team score

- home_win – 1 if home team won, else 0

- season – NBA season year

  ---

 ### Notes

The scraper is rate-limited to avoid stressing the source website

Intended for personal, academic, or research use

Data is cached locally once scraped

### License

This project is licensed under the Apache 2.0 License.
See the LICENSE file for details

