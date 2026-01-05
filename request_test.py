import cloudscraper

URL = "https://www.basketball-reference.com/leagues/NBA_2026_games-november.html"

scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "windows", #to fool the website and firewall into thinking this is a real user
        "mobile": False
    }
)

r = scraper.get(URL)

print("Status Code:", r.status_code) #200 is good 403 is fail
print("HTML length:", len(r.text)) #should be 200000+
print(r.text[:300]) # first 300 string chars of the webpage
