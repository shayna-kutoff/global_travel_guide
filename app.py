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
import folium
from streamlit_folium import st_folium


# coordinates for all destinations so they could appear on the map
city_coordinates = {
"Paris": (48.8566, 2.3522),
"Tokyo": (35.6762, 139.6503),
"New York City": (40.7128, -74.0060),
"London": (51.5074, -0.1278),
"Rome": (41.9028, 12.4964),
"Barcelona": (41.3851, 2.1734),
"Dubai": (25.2048, 55.2708),
"Singapore": (1.3521, 103.8198),
"Sydney": (-33.8688, 151.2093),
"Los Angeles": (34.0522, -118.2437),
"Bangkok": (13.7563, 100.5018),
"Istanbul": (41.0082, 28.9784),
"Amsterdam": (52.3676, 4.9041),
"Hong Kong": (22.3193, 114.1694),
"Seoul": (37.5665, 126.9780),
"Berlin": (52.5200, 13.4050),
"Toronto": (43.6532, -79.3832),
"San Francisco": (37.7749, -122.4194),
"Cape Town": (-33.9249, 18.4241),
"Rio de Janeiro": (-22.9068, -43.1729)
}

st.title("🌍 Global Travel Guide")
st.subheader("Find your perfect vacation destination")

# create city dropdown that starts blank
cities = get_all_cities()
selected_city = st.selectbox("Choose a destination",[""] + cities)

# buttons to take user to destination page
column1, column2 = st.columns(2)  # buttons are next to each other
with column1:
    if st.button("🌍 Take me there!"):
        if selected_city == "":  # display warning if no city is selected
            st.warning("Please select a destination first!")
        else:
            st.session_state["selected_city"] = selected_city
            st.switch_page("pages/destination.py")
with column2:
    if st.button("🎲 Surprise me!"):
        random_city = random.choice(cities)  # the chosen city should be randomly generated
        st.session_state["selected_city"]=random_city  # brings the chosen destination to the destination page
        st.switch_page("pages/destination.py")

# map with all the destinations
st.subheader("20 Most Popular Destinations")
my_map = folium.Map(location=[20, 0], zoom_start=2)  # map centered on world
for city, coords in city_coordinates.items():
    # add pin for each city and show the name when you hover over it
    folium.Marker(
    location=coords,
    popup=city,
    tooltip=city
).add_to(my_map)
st_folium(my_map, width=700, height=400)

# implement the crud methods of insert new city, update description, or delete a city
st.subheader("Manage Destinations")
tab1, tab2, tab3 = st.tabs(["Add City", "Delete City", "Update City"])

with tab1:  # add a new city
    new_name = st.text_input("City Name")
    new_desc = st.text_area("Description")
    new_pop = st.text_input("Population")
    if st.button("Add City"):
        from database import insert_new_city
        result = insert_new_city(new_name, new_desc, new_pop)
        if result:
            st.success("City added!")
        else:
            st.error("Could not add city!")

with tab2:  # delete a city
    city_to_delete = st.selectbox("Select city to delete", cities)
    if st.button("Delete City"):
        from database import delete_city
        result = delete_city(city_to_delete)
        if result:
            st.success("City Deleted")
        else:
            st.error("City not found")

with tab3:  # update a city
    city_to_update = st.selectbox("Select city to update", cities)
    updated_desc = st.text_area("New Description")
    if st.button("Update Description"):
        from database import update_city
        result = update_city(city_to_update, updated_desc)
        if result:
            st.success("Description Updated")
        else:
            st.error("Could not update")

# chat bot for ideas of where to go
st.subheader("Not sure where to go? Ask our AI Travel Advisor!")
get_response("You are a friendly travel advisor helping users decide where to go on vacation. Suggest destinations based on their preferences, budget, and interests.",
"Where should I go on vacation?", chat_key="main_messages")
