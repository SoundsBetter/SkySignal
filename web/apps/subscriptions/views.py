from rest_framework import viewsets, permissions

from .models import Subscription
from .serializers import SubscriptionSerializer


class SubscriptionsViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')
        if user_pk is not None:
            return Subscription.objects.filter(user=user_pk)
        return Subscription.objects.none()

    def preform_create(self, serializer):
        serializer.save(user=self.request.user)