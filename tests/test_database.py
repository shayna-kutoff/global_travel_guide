"""
test_database.py
Tests for database.py functions.
Ensures data is correctly retrieved from the SQLite database.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # where to find my data
from database import get_all_cities, get_city_info, get_landmarks

def test_get_all_cities():
    # test to make sure all the cities are scraped into lists
    cities = get_all_cities()
    assert isinstance(cities, list)
    assert len(cities) > 0

def test_get_city_info():
    # test to make sure city info comes out correct, positon 1 is the name etc.
    result = get_city_info("Paris")
    assert result is not None
    assert result[1] == "Paris"

def test_get_landmarks():
    # test to make sure landmarks are scraped into list
    result = get_landmarks("Paris")
    assert isinstance (result, list)
