from django.contrib import admin

from .models import City, WeatherData

admin.site.register(City)
admin.site.register(WeatherData)

