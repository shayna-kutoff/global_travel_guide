
"""
database.py
Handles all reading from the SQLite travel database.
Used by the Streamlit app to fetch city info, landmarks, and city names.
"""
import sqlite3
import os
DB_PATH = os.environ.get("TEST_DB", "data/travel.db")

def get_all_cities():
    """Returns a list of all city names from the database"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM cities")
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows]

def insert_new_city(name, description, population):
    """ Inserts a new city with description and population into the database"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if not name or not description or not population:
        conn.close()
        return False
    cur.execute("INSERT OR IGNORE INTO cities (name, description, population, image_url) VALUES (?, ?, ?, ?)", (name, description, population, None))
    conn.commit()
    conn.close()
    return True

def update_city(name, new_description):
    """ Updates an existind city's description """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id FROM cities WHERE name = ?", (name,))
    city = cur.fetchone()
    if city is None:
        conn.close()
        return False
    cur.execute("UPDATE cities SET description = ? WHERE name = ?", (new_description, name))
    conn.commit()
    conn.close()
    return True

def delete_city(name):
    """ Deletes a selected city from the database"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id FROM cities WHERE name = ?", (name,))
    city = cur.fetchone()
    if city is None:
        conn.close()
        return False  # city not found
    cur.execute("DELETE FROM cities WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    return True

def get_city_info(city_name):
    """ Returns all info for a specific city from the database"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT*FROM cities WHERE name =?", (city_name,))  # select info from cities table, ? is the parameter we give it
    row = cur.fetchone()  # fetch the info from only 1 city and save it in the row
    conn.close()
    return row

def get_landmarks(city_name):
    """ Returns the scraped data from the landmarks table """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id FROM cities WHERE name =?", (city_name,))
    city_id = cur.fetchone()[0]  # get the city id so could search using it
    cur.execute("SELECT landmark FROM landmarks WHERE city_id = ?", (city_id,))
    row = cur.fetchall()  # get all of the landmarks
    conn.close()
    return row
