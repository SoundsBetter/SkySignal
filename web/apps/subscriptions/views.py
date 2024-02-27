from rest_framework import viewsets, permissions

from .models import SubscriptionWeather
from .serializers import SubscriptionSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = SubscriptionWeather.objects.all()
