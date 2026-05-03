"""
api.py
Handles weather data retrieval from OpenWeatherMap API.
Fetches current weather and 5 day forecast for a given city.
"""
import streamlit as st
import requests

def fetch_weather(city):
    """ Fetches 5 day weather forecast from OpenWeatherMap API for a given city"""
    api_key = st.secrets["OPENWEATHER_API_KEY"]  # reads key from secrets file
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=imperial"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def parse_forecast(data):
    """ Parses raw JSON weather data and returns a clean list of daily forecasts"""
    forecast = []
    for item in data["list"]:
        date = item["dt_txt"]
        temp = item["main"]["temp"]
        chance_of_rain = item["pop"] * 100  # make it into percentage
        forecast.append({
        "date": date,
        "temp": temp,
        "rain": chance_of_rain
    })
    return forecast

def fetch_city_image(city):
    """ Fetches the main thumbnail image url for a city from Wikipedia API"""
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{city.replace(' ', '_')}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers)
        data = response.json()
        if "thumbnail" in data:
            return data["thumbnail"]["source"]
        return None
    except:
        return None
