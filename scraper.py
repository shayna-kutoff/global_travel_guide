"""
scraper.py
This scrapes travel info from Wikipedia for a list of famous tourist cities across the globe
The scraper recieves for each city:
- a short overview/description of the place
- Population
- A list of landmarks and/or attractions
- An image url (if available)
the data is cleaned and saved into SQLite db where it will be
displayed by streamlit app.
"""
import requests
from bs4 import BeautifulSoup
import sqlite3
import re
import os
# do this so could run test on db without inserting or deleting real data
DB_PATH = os.environ.get("TEST_DB", "data/travel.db")  # reads an enviroment variable so could change w/o changing code

# list of cities to scrape
cities = [
    "Paris", "Tokyo", "New York City", "London", "Rome",
    "Barcelona", "Dubai", "Singapore", "Sydney", "Los Angeles",
    "Bangkok", "Istanbul", "Amsterdam", "Hong Kong", "Seoul",
    "Berlin", "Toronto", "San Francisco", "Cape Town", "Rio de Janeiro"
]

# function to set up the database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # create location table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cities(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            description TEXT,
            population TEXT,
            image_url TEXT
        )
    """)
    # create landmark table, need it seperate bc its one to many
    cur.execute("""
        CREATE TABLE IF NOT EXISTS landmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER,
            landmark TEXT,
            FOREIGN KEY(city_id) REFERENCES cities(id)
        )
    """)
    conn.commit()
    conn.close()

# fetch the HTML content of a city's Wikipedia page
def fetch_page(city):
    url = f"https://en.wikipedia.org/wiki/{city.replace(' ', '_')}"
    # have to pretend to be normal browser so wiki will let me access
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

# parse each part of the page, 1 function at a time
# start with description
def parse_description(soup):
    # allows us to ignore everything that is not part of actual article
    content = soup.find(id="mw-content-text") or soup.find(class_="mw-parser-output")
    if not content:
        return "Description not found"
    # dig through all nested levels to find more <p> tags
    paragraphs = content.find_all('p', recursive=True)
    for p in paragraphs:
        # clean the text
        text = p.get_text().strip()
        # only return it if its a real sentance
        if len(text) > 30:
            text = re.sub(r'\[.*?\]', '', text)  # clear all of the brackets thst are interspersed in the paragraph
            return text
    return "No description available"

# parse the population
def parse_population(soup):
    # every city page in wiki has infobox which stores info about the city, we want the pop from there
    infobox = soup.find("table", class_="infobox")  # beautiful soup knows where to find it
    if not infobox:
        return None
    rows = infobox.find_all("tr")
    for i, row in enumerate(rows):  # need the position so could go to next row for actual number
        if "Population" in row.get_text():
            if i + 1< len(rows):
                next_row = rows[i +1].get_text(strip=True)
                next_row = re.sub(r'\[.*?\]', '', next_row)
                numbers = re.findall(r'[\d,]+', next_row)  # return everuthing found and make return the population num
                next_row = numbers[0] if numbers else next_row   # if first num is found return it, else use the next row
                return next_row
    return None

# parse teh landmarks
def parse_landmarks(soup):
    landmarks = []
    headers = soup.find_all(["h2", "h3"])  # collect the major sections and the subsections
    for header in headers:
        title = header.get_text().lower()
        if any(word in title for word in ["landmark", "tourism", "attractions", "sights", "points of interest", "culture", "arts", "cuisine"]):  # filter
            ul = header.find_next("ul")  # the ul comes after the header (ie unordered list under attractions)
            if ul:
                for li in ul.find_all("li"):  # the li tags are the ones before and after the attraction
                    landmarks.append(li.get_text(strip=True))
            break
    return landmarks

# now save all the parsed data to db
def save_to_db(name, description, population, image_url, landmarks):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # insert the city
    cur.execute("""
        INSERT OR IGNORE INTO cities (name, description, population, image_url)
        VALUES (?, ?, ?, ?)
    """, (name, description, population, image_url))

    # get city id for the landmarks table
    cur.execute("SELECT id FROM cities WHERE name = ?", (name,))
    city_id = cur.fetchone()[0]
    # insert landmarks into the table
    for l in landmarks:
        cur.execute("""
            INSERT INTO landmarks (city_id, landmark)
            VALUES(?, ?)
        """, (city_id, l))

    conn.commit()
    conn.close()

# function to scrape the cities and save them
def run_scraper():
    init_db()

    for city in cities:
        try:
            print(f"Scraping {city}")
            html = fetch_page(city)
            soup = BeautifulSoup(html, "html.parser")
            description = parse_description(soup)
            population = parse_population(soup)
            landmarks = parse_landmarks(soup)
            image_url = None

            save_to_db(city, description, population, image_url, landmarks)
        except sqlite3.IntegrityError:
            print(f"Skipping {city}: Already exists in database.")

    print("Scraping complete!")

if __name__ == "__main__":
    run_scraper()
