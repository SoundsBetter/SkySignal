import os
from pprint import pprint

import requests

'''
http://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}
'''

DOMAIN = "https://api.openweathermap.org/geo/1.0/direct"
API_KEY = os.environ.get('OPEN_WEATHER_API')


def fetch_city_data(
        city_name, country_code=None, state_code=None, limit=5, api_key=API_KEY
):
    query = ','.join(part for part in [city_name, state_code, country_code] if part)
    url = f"{DOMAIN}?q={query}&limit={limit}&aapid={api_key}"

    response = requests.get(url)
    pprint(response.json())

fetch_city_data("Kyiv")

