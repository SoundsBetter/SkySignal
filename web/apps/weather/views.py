from rest_framework import viewsets, permissions

from apps.weather import serializers
from apps.weather import models


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CountrySerializer
    queryset = models.Country.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CitySerializer
    queryset = models.City.objects.all()
    permission_classes = [permissions.IsAuthenticated]

class WeatherDataViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CitySerializer
    queryset = models.WeatherData.objects.all()
    permission_classes = [permissions.IsAuthenticated]

