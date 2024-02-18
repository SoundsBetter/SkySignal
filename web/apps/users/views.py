import requests
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.utils.crypto import get_random_string
from django.views.generic import TemplateView
from rest_framework import viewsets, permissions
from django.http import JsonResponse
from django.conf import settings

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = settings.GH_CALLBACK_URL
    client_class = OAuth2Client

class DevConfirmTemplateView(TemplateView):
    template_name = 'confirm_email.html'

def github_login(request):
    state = get_random_string(32)
    request.session['oauth_state'] = state
    auth_url = f"https://github.com/login/oauth/authorize?client_id={settings.GH_CLIENT_ID}&redirect_uri={settings.GH_CALLBACK_URL}&state={state}"
    return JsonResponse({'auth_url': auth_url})



def github_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    saved_state = request.session.get('oauth_state')

    if not state or state != saved_state:
        return JsonResponse({'error': 'Invalid state parameter'}, status=400)
    if code:
        token_url = 'https://github.com/login/oauth/access_token'
        payload = {
            'client_id': settings.GH_CLIENT_ID,
            'client_secret': settings.GH_SECRET,
            'code': code,
            'redirect_uri': settings.GH_CALLBACK_URL,
        }
        headers = {'Accept': 'application/json'}
        response = requests.post(token_url, data=payload, headers=headers)
        access_token = response.json().get('access_token')

        return JsonResponse({'access_token': access_token})
    else:
        return JsonResponse({'error': 'Code not provided'}, status=400)
