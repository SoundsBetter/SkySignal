import os
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv()
"""
http://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}
"""

DOMAIN = "https://api.openweathermap.org/geo/1.0/direct"
API_KEY = os.environ.get("OPEN_WEATHER_API")


def fetch_city_data(
    city_name=None, country_code=None, state_code=None, limit=5, api_key=API_KEY
):
    query = ",".join(
        part for part in [city_name, state_code, country_code] if part
    )
    url = f"{DOMAIN}?q={query}&limit={limit}&appid={api_key}"
    print(url)

    response = requests.get(url)
    data = response.json()
    print(data)
    return [city for city in data]


res = fetch_city_data(city_name="Smila", limit=2)
[print(f"{x}\n=================================") for x in res]
