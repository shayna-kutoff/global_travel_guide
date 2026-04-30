"""
app.py
Streamlit app that has a main page that helps a user to choose a travel destination
and then takes user to another page with information about that place
Uses database.py for city data, ai.py for travel suggestions,
and folium for the interactive map.
"""
import streamlit as st
import random
from database import get_all_cities
from ai import get_response

st.title("🌍 Global Travel Guide")
st.subheader("Find your perfect vacation destination")

# create city dropdown
cities = get_all_cities()
selected_city = st.selectbox("Choose a destination", cities)

# buttons to take user to destination page
column1, column2 = st.columns(2)  # buttons are next to each other
with column1:
    if st.button("Take me there!"):
        st.session_state["selected_city"]=selected_city
        st.switch_page("pages/destination.py")
with column2:
    if st.button("🎲 Surprise me!"):
        random_city = random.choice(cities)  # the chosen city should be randomly generated
        st.session_state["selected_city"]=random_city  # brings the chosen destination to the destination page
        st.switch_page("pages/destination.py")
