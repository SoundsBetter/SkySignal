from rest_framework import serializers

from .models import SubscriptionWeather


class SubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubscriptionWeather
        fields = "__all__"