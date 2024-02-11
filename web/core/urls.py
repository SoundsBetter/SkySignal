from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from apps.subscriptions import views as subscriptions_views
from apps.users import views as user_views
from apps.weather import views as weather_views

router = routers.DefaultRouter()

viewsets = [
    ("users", user_views.UserViewSet, "user"),
    ("subscriptions", subscriptions_views.SubscriptionViewSet, "subscription"),
    ("countries", weather_views.CountryViewSet, "country"),
    ("cities", weather_views.CityViewSet, "city"),
    ("weather_data", weather_views.WeatherDataViewSet, "weather_data"),

]

for prefix, viewset, basename in viewsets:
    router.register(prefix, viewset, basename)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),
    path("", include(router.urls)),
]
