# Weather App - Web App for realtime forecast

A simple web app built with Python and Django that allows users to check the weather in any city around the world using the API: OpenWeather. The app displays the current weather and a one-week forecast powered by the API: One Call.
Users can save their favorite cities using LocalStorage so no login is required to use the web. 

---

## Technologies & Requirements

- Python 3.10
- Django 5.2.7

## Features

- Basic search engine to search for any city. 
- Display options of cities if they share the name. 
- Display the current weather and a one-week forecast.
    - The current weather includes: Weather conditions, temperature, feels like temperature, humidity, wind and precipitation.
- Favorite cities stored locally, saved in the "Saved Cities" list. 


---

## Installation

- Clone the repository 
git clone <YOUR_REPO_URL>
cd weatherapp

- Create and activate the virtual environment 
python -m venv .venv
source .venv/bin/activate  

- Install dependencies
pip install -r requirements.txt

- Create a .env file in the project root and set up for usage.

DEBUG=True
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=127.0.0.1,localhost

WEATHER_API_KEY=your_openweather_api_key
WEATHER_BASE_URL=https://api.openweathermap.org/data/2.5
WEATHER_ONECALL_URL=https://api.openweathermap.org/data/3.0/onecall
WEATHER_UNITS=metric

- Run migrations and start the server
python manage.py migrate
python manage.py runserver

- Notes: 
    - WEATHER_API_KEY is YOUR API key.

## How It Works

- The user search for a city in the main page.
- With the API connection, the web app shows the options.
- Django calls OpenWeather Current Weather API to get coordinates and conditions.
- Coordinates are passed to One Call API to fetch the 7-day forecast.
- User enter in the desired city and the data is normalized using the templates. 
- There is an optional button that allows the user to save the city as a favorite.

---

## Learned:
(This was my first Django project with an external API)
- Learned to integrate external APIs into a Django app.
- Learned to structure a large multi-app Django project.
- Learned to use Local Storage to avoid login. 
- Learned to normalize API data efficiently with Django templates.
- Learned to combine backend logic with a simple frontend project.
---

## License 
MIT © yberside. See LICENSE.
