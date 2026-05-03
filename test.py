from scraper import fetch_page
from bs4 import BeautifulSoup
html = fetch_page("Paris")
soup = BeautifulSoup(html, "html.parser")
headers = soup.find_all(["h2", "h3"])
for header in headers:
    title = header.get_text().lower()
    if "museum" in title:
        print("FOUND:", header.get_text())
        next_sibling = header.find_next_sibling()
        count = 0
        while next_sibling and count < 5:
            print(next_sibling.name, ":", next_sibling.get_text(strip=True)[:50])
            if next_sibling.name in ["h2", "h3"]:
                break
            next_sibling = next_sibling.find_next_sibling()
            count += 1
