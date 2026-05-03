"""
test_scraper.py
Tests for scraper.py functions.
tests web scraping, parsing and storing
uses mocking
"""
import os
os.environ["TEST_DB"] = "data/test_travel.db"
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bs4 import BeautifulSoup
import sqlite3
from scraper import init_db, parse_description, parse_landmarks, parse_population, fetch_page, save_to_db, run_scraper

def test_init_db():
    # check that function creates correct tables
    conn = sqlite3.connect("data/test_travel.db")
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cur.fetchall()]
    conn.close()
    assert "cities" in tables
    assert "landmarks" in tables

def test_parse_description():
    html = """
    <div id="mw-content-text">
    <p>Paris is a beautiful city in France with many attractions and landmarks.</p>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = parse_description(soup)
    assert isinstance(result, str)
    assert len(result) > 0
    assert "Paris" in result

def test_parse_landmarks():
    html = """
    <h2>Landmarks</h2>
    <ul>
    <li>Eiffel Tower</li>
    <li>Louvre Museum</li>
    <li>Notre Dame</li>
    </ul>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = parse_landmarks(soup)
    assert isinstance(result, list)
    assert len(result) > 0
    assert "Eiffel Tower" in result

def test_parse_population():
    # create a fake html to test
    html = """
    <table class="infobox">
    <tr><td>Area</td></tr>
    <tr><td>52 km²</td></tr>
    <tr><td>Population</td></tr>
    <tr><td>2,161,000</td></tr>
    </table>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = parse_population(soup)
    assert result is not None
    assert "2,161,000" in result

def test_save_to_db():
    save_to_db("TestCity", "A test description", "1,000,000", None, ["Test Landmark"])
    conn = sqlite3.connect("data/test_travel.db")
    cur = conn.cursor()
    cur.execute("SELECT name FROM cities WHERE name = 'TestCity'")
    result = cur.fetchone()
    conn.close()
    assert result is not None
    assert result[0] == "TestCity"

