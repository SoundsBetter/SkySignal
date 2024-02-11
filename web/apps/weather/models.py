from django.db import models
from django.db.models import JSONField


class Country(models.Model):
    country_code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    official_name = models.CharField(max_length=100, null=True)


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    region = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return f"{self.name} in {self.country.name}"

class WeatherData(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    data = JSONField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WeatherData for {self.city.name} at {self.datetime}"




