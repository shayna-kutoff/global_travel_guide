
"""
database.py
Handles all reading from the SQLite travel database.
Used by the Streamlit app to fetch city info, landmarks, and city names.
"""
import sqlite3

# function to get all the cities to fill the dropdown
def get_all_cities():
    conn = sqlite3.connect("data/travel.db")
    cur = conn.cursor()
    cur.execute("SELECT name FROM cities")
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows]

# function to pull the information from the cities table, based on the city name chosen
def get_city_info(city_name):
    conn = sqlite3.connect("data/travel.db")
    cur = conn.cursor()
    cur.execute("SELECT*FROM cities WHERE name =?",(city_name,))  # select info from cities table, ? is the parameter we give it
    row = cur.fetchone()  # fetch the info from only 1 city and save it in the row
    conn.close()
    return row

def get_landmarks(city_name):
    conn = sqlite3.connect("data/travel.db")
    cur = conn.cursor()
    cur.execute("SELECT id FROM cities WHERE name =?",(city_name,))
    city_id = cur.fetchone()[0]  # get the city id so could search using it
    cur.execute("SELECT landmark FROM landmarks WHERE city_id = ?", (city_id,))
    row = cur.fetchall()  # get all of the landmarks
    conn.close()
    return row
