from rest_framework import serializers

from .models import City, WeatherData
from .services import WeatherService


class CitySerializer(serializers.HyperlinkedModelSerializer):
    region = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    class Meta:
        model = City
        fields = ["url", 'id', 'name', 'country', "region", "lat", "lon"]


class WeatherDataSerializer(serializers.HyperlinkedModelSerializer):
    service = WeatherService()
    class Meta:
        model = WeatherData
        fields = '__all__'

    def create(self, validated_data):
        city_instance = validated_data.get("city")
        data = self.service.fetch_weather_data(
            city_instance.lat, city_instance.lon
        )
        return WeatherData.objects.create(
            city=city_instance, data=data
        )

