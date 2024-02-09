from django.db import models
from django.db.models import JSONField


class Country(models.Model):
    name = models.CharField(max_length=100)


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} in {self.country.name}"

class WeatherData(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    data = JSONField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WeatherData for {self.city.name} at {self.datetime}"




