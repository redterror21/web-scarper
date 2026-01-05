import cloudscraper
import pandas as pd
from bs4 import BeautifulSoup, Comment

URL = "https://www.basketball-reference.com/leagues/NBA_2026_games-october.html"

scraper = cloudscraper.create_scraper()
html = scraper.get(URL).text
soup = BeautifulSoup(html, "html.parser")

#  Find schedule table (direct or commented)
table = soup.find("table", {"id": "schedule"})

if table is None:
    comments = soup.find_all(string=lambda t: isinstance(t, Comment))
    for c in comments:
        if 'table id="schedule"' in c:
            table = BeautifulSoup(c, "html.parser").find("table", {"id": "schedule"})
            break

assert table is not None, "Schedule table not found"

#  Helper to read data-stat safely
def get_cell(row, stat):
    cell = row.find("td", {"data-stat": stat})
    return cell.text.strip() if cell else ""

#  Extract games
games = []

for row in table.find("tbody").find_all("tr"):
    if row.get("class") == ["thead"]:
        continue

    away_pts = get_cell(row, "visitor_pts")
    home_pts = get_cell(row, "home_pts")

    # skip future games
    if away_pts == "" or home_pts == "":
        continue

    games.append({
        "date": get_cell(row, "date_game"),
        "away_team": get_cell(row, "visitor_team_name"),
        "away_pts": int(away_pts),
        "home_team": get_cell(row, "home_team_name"),
        "home_pts": int(home_pts),
        "home_win": int(int(home_pts) > int(away_pts))
    })

df = pd.DataFrame(games)

print(df.head(3))
print("Total games scraped:", len(df))
