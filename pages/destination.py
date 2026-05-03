"""
destination.py
Displays information and landmarks about the chosen place
Uses database.py for city info and landmarks,api.py for weather forecast,
and ai.py for travel suggestions about the specific city.
"""

import streamlit as st
from database import get_city_info, get_landmarks
from api import fetch_weather, parse_forecast
import plotly.express as px
import pandas as pd
from ai import get_response

# if no city was selected, go straight to home page
if "selected_city" not in st.session_state:
    st.switch_page("app.py")
city = st.session_state["selected_city"]
# button to take user back to main menu, clear chat
if st.button("Back to Main Menu"):
    st.session_state["destination_messages"] = []
    st.switch_page("app.py")
st.title(f"🌍 {city}")

# call my database functions to get info about city
city_info = get_city_info(city)
landmarks = get_landmarks(city)
st.write(city_info[2])  # details
st.subheader("Population")
st.write(city_info[3])  # population
# display landmarks
st.subheader("Landmarks and Attractions")
if landmark in landmarks:
    st.write(f"• {landmark[0]}")
else:
    st.info("No landmarks data available for this city.")

# display weather forecast
st.subheader("5 Day Weather Forecast")
weather_data = fetch_weather(city)
forecast = parse_forecast(weather_data)
daily_forecast = []
for weather in forecast:  # loop through forecast and only keeep 1 data per day
    if "12:00:00" in weather["date"]:
        daily_forecast.append(weather)
for weather in daily_forecast:  # now loop through daily forecast list and print
    st.write(f"{weather['date'][:10]} — 🌡️ {weather['temp']}*F — 🌧️ {weather['rain']:.0f}% chance of rain")

# chart to display header
st.subheader("📊 Weather This Week")
df = pd.DataFrame(daily_forecast)  # convert list into table to work with
df['date'] = df['date'].str[:10]  # display the clean date data
# create a line chart with x and y axis, title and labels
fig = px.line(df,x='date', y='temp', title=f'Temperature in {city} this week', labels={'date':'Date', 'temp': 'Temperature(*F)'})
st.plotly_chart(fig)  # display the chart

# ai chatbot about destination
st.subheader("Ask Our Travel AI Chatbot")
get_response(f"You are a travel advisor giving detailed advice about {city}. Tell the user what to do, eat, and see there.",
"Ask me anything about " + city + "!", chat_key="destination_messages")
