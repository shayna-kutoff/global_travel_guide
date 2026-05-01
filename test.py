from scraper import fetch_page
from bs4 import BeautifulSoup
html = fetch_page("New York City")
soup = BeautifulSoup(html, "html.parser")
headers = soup.find_all(["h2", "h3"])
for header in headers:
    title = header.get_text().lower()
    if "culture" in title:
        print("FOUND:", header.get_text())
    ul = header.find_next("ul")
    if ul:
        print(ul.get_text(strip=True)[:200])