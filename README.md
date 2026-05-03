# 🌍 Global Travel Guide
A Streamlit web application that helps users discover and plan their perfect vacation destination. Browse 20 of the world's most popular cities, get real-time weather forecasts, explore landmarks, and chat with an AI travel advisor.
Live App: https://globaltravelguide-zgk4kbc4wwwxddnrusifyp.streamlit.app

![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

## 🛠️ Setup & Installation
1. Clone the repository:
git clone https://github.com/shayna-kutoff/global_travel_guide.git
cd global_travel_guide
2. Install dependencies:
pip install -r requirements.txt
3. Set up your secrets file:
Create a file at .streamlit/secrets.toml and add:
OPENWEATHER_API_KEY = "your_key"
AZURE_OPENAI_ENDPOINT = "your_endpoint"
AZURE_OPENAI_API_KEY = "your_key"
AZURE_OPENAI_MODEL = "your_model"
4. Run the scraper to populate the database:
python scraper.py
5. Run the app:
streamlit run app.py

## 📖 How to Use
### Using the Deployed App
Visit the live app at https://globaltravelguide-zgk4kbc4wwwxddnrusifyp.streamlit.app
No installation needed — the app runs directly in your browser.
Note: The AI chatbot requires valid Azure OpenAI credentials configured in Streamlit's secrets manager.
### Main Page
- Browse the interactive world map showing all 20 destinations
- Select a city from the dropdown menu
- Click "Take me there!" to view detailed information
- Click "Surprise me!" for a random destination
- Chat with the AI Travel Advisor for personalized recommendations
### Destination Page
- View a description and population of the city
- Click the Wikipedia link to learn more about the city
- Check the 5 day weather forecast
- View an interactive temperature chart
- Ask the AI chatbot questions about the destination
- Click "Back to Main Menu" to return home
### Managing Destinations
At the bottom of the main page you can manage the database:
- Add City tab — add a new destination by entering a name, description and population
- Delete City tab — remove a destination from the database
- Update City tab — suggest a new description for an existing city

## 🤖 AI Integration
This app uses Azure OpenAI (GPT) for two features:
1. Main Page Travel Advisor — helps users decide where to go based on their preferences, budget, and interests
2. Destination Page Chatbot — answers specific questions about the chosen city including things to do, eat, and see
The AI is accessed via the OpenAI Python library using Azure credentials stored securely in Streamlit's secrets manager. Users interact with the AI through a chat interface built with Streamlit's st.chat_input and st.chat_message components.

## 🧪 Testing
Run the test suite:
pytest tests/
Or using python -m pytest:
python -m pytest tests/
Run with coverage report:
pytest tests/ --cov=. --cov-report=term-missing
Generate HTML coverage report:
pytest tests/ --cov=. --cov-report=html
Tests achieve > 60% coverage and cover:
- Database functions (CRUD operations)
- Scraper parsing functions
- Weather API parsing

## 📦 Dependencies
See requirements.txt for full list. Main libraries:
- streamlit
- requests
- beautifulsoup4
- openai
- plotly
- pandas
- folium
- streamlit-folium
