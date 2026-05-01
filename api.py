"""
api.py
Handles weather data retrieval from OpenWeatherMap API.
Fetches current weather and 5 day forecast for a given city.
"""
import streamlit as st
import requests

# function to fetch the weather for parameter city
def fetch_weather(city):
    api_key = st.secrets["OPENWEATHER_API_KEY"]  # reads key from secrets file
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=imperial"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# function to parse the json info from weather app
def parse_forecast(data):
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
