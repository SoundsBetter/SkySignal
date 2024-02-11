"""
http://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}
"""
import pycountry
import requests
from django.conf import settings

from apps.weather.models import Country

DOMAIN = "https://api.openweathermap.org/geo/1.0/direct"
API_KEY = settings.OPEN_WEATHER_API_KEY


def create_or_get_country(country_name: str) -> Country | None:
    try:
        country = pycountry.countries.lookup(country_name)
    except LookupError:
        return None

    try:
        existing_country = Country.objects.get(country_code=country.alpha_2)
    except Country.DoesNotExist:
        country_data = {
            'country_code': country.alpha_2,
            'name': country.name,
        }
        if hasattr(country, 'official_name'):
            country_data['official_name'] = country.official_name

        return Country.objects.create(**country_data)
    return existing_country

def fetch_city_data(
    city_name=None, country_code=None, state_code=None, limit=5
):
    query = ",".join(
        part for part in [city_name, state_code, country_code] if part
    )
    url = f"{DOMAIN}?q={query}&limit={limit}&appid={API_KEY}"
    print(url)
    response = requests.get(url)
    data = response.json()
    print(data)
    return [city for city in data]
