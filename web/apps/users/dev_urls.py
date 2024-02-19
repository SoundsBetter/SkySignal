from django.urls import path, re_path

from .dev_views import DevConfirmTemplateView, github_get_link, github_callback

urlpatterns = [
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$',
        DevConfirmTemplateView.as_view(),
        name='account_confirm_email',
    ),
    path('github/link/', github_get_link, name='github_get_link'),
    path('github/login/callback/', github_callback, name='github_callback'),
]
