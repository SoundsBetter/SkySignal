import requests
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.utils.crypto import get_random_string
from django.views.generic import TemplateView
from rest_framework import viewsets, permissions
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class DevConfirmTemplateView(TemplateView):
    template_name = 'confirm_email.html'


