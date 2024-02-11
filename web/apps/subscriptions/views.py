from rest_framework import viewsets, permissions

from .models import Subscription
from .serializers import SubscriptionSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Subscription.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
