from django.urls import path, include, re_path

from .views import DevConfirmTemplateView, GitHubLogin

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path(
        "registration/", include("dj_rest_auth.registration.urls")
    ),
    path("github/", GitHubLogin.as_view(), name="github_login"),
    path('accounts/', include('allauth.urls')),
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$',
        DevConfirmTemplateView.as_view(),
        name='account_confirm_email',
    ),
]