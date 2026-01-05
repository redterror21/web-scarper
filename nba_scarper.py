import time
import pandas as pd
import cloudscraper
from bs4 import BeautifulSoup, Comment

BASE_URL = "https://www.basketball-reference.com"
SEASONS = [2022, 2023, 2024, 2025, 2026]

MONTHS = [
    "october", "november", "december",
    "january", "february", "march", "april"
]

scraper = cloudscraper.create_scraper()

def find_schedule_table(html):
    soup = BeautifulSoup(html, "html.parser")

    # Try direct table
    table = soup.find("table", {"id": "schedule"})
    if table:
        return table

    # Try commented table
    comments = soup.find_all(string=lambda t: isinstance(t, Comment))
    for c in comments:
        if 'table id="schedule"' in c:
            comment_soup = BeautifulSoup(c, "html.parser")
            table = comment_soup.find("table", {"id": "schedule"})
            if table:
                return table

    return None


def scrape_month(season, month):
    url = f"{BASE_URL}/leagues/NBA_{season}_games-{month}.html"
    print(f"Scraping: {url}")

    r = scraper.get(url)
    if r.status_code != 200:
        return []

    table = find_schedule_table(r.text)
    if table is None:
        return []

    games = []

    def get(row, stat):
        cell = row.find("td", {"data-stat": stat})
        return cell.text.strip() if cell else ""

    for row in table.find("tbody").find_all("tr"):
        if row.get("class") == ["thead"]:
            continue

        away_pts = get(row, "visitor_pts")
        home_pts = get(row, "home_pts")

        if away_pts == "" or home_pts == "":
            continue

        games.append({
            "date": get(row, "date_game"),
            "away_team": get(row, "visitor_team_name"),
            "away_pts": int(away_pts),
            "home_team": get(row, "home_team_name"),
            "home_pts": int(home_pts),
            "home_win": int(int(home_pts) > int(away_pts)),
            "season": season
        })

    time.sleep(2)  # IMPORTANT: be polite
    return games


def scrape_season(season):
    season_games = []
    for month in MONTHS:
        season_games.extend(scrape_month(season, month))
    print(f"Season {season}: {len(season_games)} games")
    return season_games


def main():
    all_games = []

    for season in SEASONS:
        all_games.extend(scrape_season(season))

    df = pd.DataFrame(all_games)

    # Basic sanity checks
    assert df.isnull().sum().sum() == 0
    assert len(df) > 5000

    df.to_csv("data/nba_games_last_5_years.csv", index=False)
    print("Saved:", len(df), "games")


if __name__ == "__main__":
    main()
