"""
test_api.py
Tests for api.py functions.
Tests weather data parsing using mocking so dont have to do real api call
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # where to find my data
from unittest.mock import patch
from api import parse_forecast, fetch_weather, fetch_city_image

def test_fetch_weather():
    with patch("api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {
        "list": [{
        "dt_txt": "2024-01-15 12:00:00",
        "main": {"temp": 72.5},
        "pop": 0.4
        }]}
        mock_get.return_value.raise_for_status = lambda: None
        result = fetch_weather("Paris")
    assert result is not None
    assert "list" in result

def test_parse_forecast():
    fake_data = {
    "list": [{
    "dt_txt": "2024-01-15 12:00:00",
    "main": {"temp": 72.5},
    "pop": 0.4
    }]}
    result = parse_forecast(fake_data)
    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0]["temp"] == 72.5
    assert result[0]["rain"] == 40.0

def test_fetch_city_image():
    with patch("api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {
        "thumbnail": {
        "source": "https://example.com/image.jpg"
        }
        }
        result = fetch_city_image("Paris")
    assert result == "https://example.com/image.jpg"

def test_fetch_city_image_no_thumbnail():
    with patch("api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {}
        mock_get.return_value.raise_for_status = lambda: None
        result = fetch_city_image("Paris")
        assert result is None

def test_fetch_city_image_exception():
    with patch("api.requests.get") as mock_get:
        mock_get.side_effect = Exception("Network error")
        result = fetch_city_image("Paris")
        assert result is None
