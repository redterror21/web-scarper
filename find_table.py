import cloudscraper
from bs4 import BeautifulSoup, Comment

URL = "https://www.basketball-reference.com/leagues/NBA_2026_games-november.html"

scraper = cloudscraper.create_scraper()
html = scraper.get(URL).text

soup = BeautifulSoup(html, "html.parser")

# STEP 1: try direct table
table = soup.find("table", {"id": "schedule"})

if table:
    print("Schedule table found (direct HTML)")
else:
    # STEP 2: try commented tables
    comments = soup.find_all(string=lambda t: isinstance(t, Comment))
    for c in comments:
        if 'table id="schedule"' in c:
            comment_soup = BeautifulSoup(c, "html.parser")
            table = comment_soup.find("table", {"id": "schedule"})
            if table:
                print("Schedule table found (inside comments)")
                break

# FINAL CHECK
if table is None:
    print(" Schedule table NOT found on this page")
else:
    headers = [th.text.strip() for th in table.find_all("th")]
    print("Headers:", headers)
