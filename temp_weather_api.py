import os
import requests
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

DOMAIN = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = os.environ.get("OPEN_WEATHER_API")
CITY_NAME = "Kyiv"

def fetch_weather_by_city_name(city_name, api_key):
    url = f"{DOMAIN}?q={city_name}&appid={api_key}&units=metric&lang=ua"

    response = requests.get(url)
    pprint(response.json())


fetch_weather_by_city_name(CITY_NAME, API_KEY)
