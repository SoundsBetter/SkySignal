from rest_framework import serializers

from apps.weather import models


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = '__all__'

class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = '__all__'