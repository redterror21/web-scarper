import cloudscraper

URL = "https://www.basketball-reference.com/leagues/NBA_2026_games-november.html"

scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "windows",
        "mobile": False
    }
)

r = scraper.get(URL)

print("Status Code:", r.status_code)
print("HTML length:", len(r.text))
print(r.text[:300])
