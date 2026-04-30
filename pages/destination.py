"""
destination.py
Displays information and landmarks about the chosen place
Uses database.py for city info and landmarks,api.py for weather forecast,
and ai.py for travel suggestions about the specific city.
"""

import streamlit as st
from database import get_city_info, get_landmarks

# if no city was selected, go straight to home page
if "selected_city" not in st.session_state:
    st.switch_page("app.py")
city = st.session_state["selected_city"]
# button to take user back to main menu
if st.button("Back to Main Menu"):
    st.switch_page("app.py")
st.title(f"🌍 {city}")

# call my database functions to get info about city
city_info = get_city_info(city)
landmarks = get_landmarks(city)
st.write(city_info[2])  # details
st.write(city_info[3])  # population
