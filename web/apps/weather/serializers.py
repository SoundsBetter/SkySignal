from rest_framework import serializers

from .models import City, WeatherData

class CitySerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(required=True)
    country = serializers.CharField(required=False)
    state = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    lat = serializers.FloatField(required=False)
    lon = serializers.FloatField(required=False)
    class Meta:
        model = City
        fields = ["url", 'id', 'name', 'country', "state", "lat", "lon"]


class WeatherDataSerializer(serializers.HyperlinkedModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    class Meta:
        model = WeatherData
        fields = '__all__'

