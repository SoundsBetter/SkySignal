from django.urls import path, include, re_path

from .views import GitHubLogin

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path(
        "registration/", include("dj_rest_auth.registration.urls")
    ),
    path("github/login/", GitHubLogin.as_view(), name="github_login"),
    path("", include("allauth.urls")),
]
