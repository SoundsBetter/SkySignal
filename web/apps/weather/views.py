from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response

from .serializers import CitySerializer, WeatherDataSerializer
from .models import City, WeatherData
from .services import CityService


class CityViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    service = CityService()

    def create(self, request, *args, **kwargs):
        data = request.data
        name = data.get("name")
        country = data.get("country", None)
        state = data.get("region", None)
        city = self.service.fetch_city_data(
            name=name,
            country=country,
            state=state,
        )
        if isinstance(city, list):
            return Response(city, status=status.HTTP_300_MULTIPLE_CHOICES)

        serializer = self.get_serializer(data=city)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"error": "City not found"}, status=status.HTTP_404_NOT_FOUND
        )


class WeatherDataViewSet(viewsets.ModelViewSet):
    serializer_class = WeatherDataSerializer
    queryset = WeatherData.objects.all()
    permission_classes = [permissions.IsAuthenticated]
