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
        payload = {"q": query, "limit": limit, "appid": self.api_key}
        response = requests.get(self.domain, params=payload)
        city_data = response.json()
        if not city_data:
            return None
        return city_data[0]


class WeatherDataService:
    def __init__(self):
        self.api_key = settings.OPEN_WEATHER_API_KEY
        self.domain = settings.OPEN_WEATHER_DOMAIN

    def fetch_weather_data(
            self, lat, lon
    ):
        payload = {"lat": lat, "lon": lon, "appid": self.api_key}
        response = requests.get(self.domain, params=payload)
        weather_data = response.json()
        if not weather_data:
            return None
        return weather_data
