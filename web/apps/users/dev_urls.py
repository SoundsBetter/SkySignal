from django.urls import path, include, re_path

from .dev_views import DevConfirmTemplateView

urlpatterns = [
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$',
        DevConfirmTemplateView.as_view(),
        name='account_confirm_email',
    ),

]
