from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework.routers import DefaultRouter

from apps.subscriptions import views as subscriptions_views
from apps.users import views as user_views
from apps.weather import views as weather_views

router = DefaultRouter()

viewsets = [
    ("users", user_views.UserViewSet, "user"),
    (
        "subscriptions",
        subscriptions_views.SubscriptionViewSet,
        "subscriptionweather",
    ),
    ("cities", weather_views.CityViewSet, "city"),
    ("weatherdata", weather_views.WeatherDataViewSet, "weatherdata"),
]

for prefix, viewset, basename in viewsets:
    router.register(prefix, viewset, basename)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("auth/", include("apps.users.dev_urls")),
    path("auth/", include("apps.users.urls")),

]

