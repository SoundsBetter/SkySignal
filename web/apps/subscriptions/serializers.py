from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Subscription
from ..weather.models import Country, City
from ..weather.utils import fetch_city_data, create_or_get_country


class SubscriptionSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(write_only=True, required=False)
    city_name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Subscription
        fields = "__all__"
        extra_kwargs = {"city": {"read_only": True}}

    def create(self, validated_data):
        city_name = validated_data.pop("city_name", None)
        country_name = validated_data.pop("country_name", None)

        # country = get_object_or_404(Country, name=country_name)
        if country_name is not None:
            country = Country.objects.filter(name=country_name)
            if not country:
                country = create_or_get_country(country_name)
                if not country:
                    raise serializers.ValidationError("Country not found")


        city = City.objects.filter(country=country, name=city_name)
        if not city:
            fetch_city_data(city_name, country_name)
            raise serializers.ValidationError("City not found")
        subscription = Subscription.objects.create(city=city, **validated_data)
        return subscription
