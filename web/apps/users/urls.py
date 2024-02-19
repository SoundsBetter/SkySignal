from django.urls import path, include, re_path

from .views import DevConfirmTemplateView, GitHubLogin, github_get_link, github_get_callback
urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path(
        "registration/", include("dj_rest_auth.registration.urls")
    ),
    path("github/login/", GitHubLogin.as_view(), name="github_login"),
    path("github/login/link/", github_get_link, name="github_login"),
    path("github/login/callback/", github_get_callback, name="github_callback"),
    path("", include("allauth.urls")),
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$',
        DevConfirmTemplateView.as_view(),
        name='account_confirm_email',
    ),
]
