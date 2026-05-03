"""
test_database.py
Tests for database.py functions.
Ensures data is correctly retrieved from the SQLite database.
"""
import os
os.environ["TEST_DB"] = "data/test_travel.db"
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # where to find my data
import pytest
from database import get_all_cities, get_city_info, get_landmarks, insert_new_city, delete_city, update_city

# set up test database
@pytest.fixture(autouse=True)
def setup_db():
    from scraper import init_db
    init_db()

def test_get_all_cities():
    # test to make sure all the cities are scraped into lists
    insert_new_city("Paris", "Paris is a beautiful city", "2,000,000")
    cities = get_all_cities()
    assert isinstance(cities, list)
    assert len(cities) > 0

def test_get_city_info():
    # test to make sure city info comes out correct, positon 1 is the name etc.
    insert_new_city("Paris", "Paris is a beautiful city", "2,000,000")
    result = get_city_info("Paris")
    assert result is not None
    assert result[1] == "Paris"

def test_get_landmarks():
    # test to make sure landmarks are scraped into list
    insert_new_city("Paris", "Paris is a beautiful city", "2,000,000")
    result = get_landmarks("Paris")
    assert isinstance (result, list)

def test_insert_new_city():
    result = insert_new_city("TestCity2", "An epic city", "1,000,000")
    assert result == True

def test_delete_city():
    insert_new_city("CityToDelete", "An epic city", "500,000")
    result = delete_city("CityToDelete")
    assert result == True

def test_delete_city_not_found():
    result = delete_city("FakeCity123")
    assert result == False

def test_update_city():
    insert_new_city("CityToUpdate", "An epic city to update", "100,000")
    result = update_city("CityToUpdate", "The city has been updated")
    assert result == True
