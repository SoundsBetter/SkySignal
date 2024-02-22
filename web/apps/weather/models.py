from django.db import models
from django.db.models import JSONField


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=3)
    state = models.CharField(max_length=255, blank=True, null=True)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return f"{self.name} in {self.country} with {self.lat=} and {self.lon=}"


class WeatherData(models.Model):
    city = models.ForeignKey(
        "City", on_delete=models.CASCADE, related_name="weather_data_set"
    )
    data = JSONField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WeatherData for {self.city.name} at {self.datetime}"
