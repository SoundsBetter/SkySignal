import requests
from django.conf import settings


class CityService:
    def __init__(self):
        self.api_key = settings.OPEN_WEATHER_API_KEY
        self.domain = settings.OPEN_GEO_DOMAIN

    def fetch_city_data(
            self, name=None, country=None, state=None, limit=5
    ):
        query = ",".join(
            part for part in [name, state, country] if part
        )
        url = f"{self.domain}?q={query}&limit={limit}&appid={self.api_key}"
        response = requests.get(url)
        data = response.json()
        if not data:
            return None
        # if len(data) > 1:
        #     return data
        return data[0]


class WeatherService:
    def __init__(self):
        self.api_key = settings.OPEN_WEATHER_API_KEY
        self.domain = settings.OPEN_WEATHER_DOMAIN

    def fetch_weather_data(
            self, lat, lon
    ):
        url = f"{self.domain}?lat={lat}&lon={lon}&appid={self.api_key}"
        response = requests.get(url)
        data = response.json()
        if not data:
            return None
        return data
