import requests
from django.utils.crypto import get_random_string
from django.views.generic import TemplateView
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response



class DevConfirmTemplateView(TemplateView):
    template_name = 'confirm_email.html'


@api_view(["GET"])
def github_get_link(request):
    state = get_random_string(32)
    request.session['oauth_state'] = state
    auth_url = f"https://github.com/login/oauth/authorize?client_id={settings.GH_CLIENT_ID}&redirect_uri={settings.GH_CALLBACK_URL}&state={state}"
    return Response(auth_url)

@api_view(["GET"])
def github_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    saved_state = request.session.get('oauth_state')

    if not state or state != saved_state:
        return Response({'error': 'Invalid state parameter'}, status=400)
    return Response(code)
    # if code:
    #     token_url = 'https://github.com/login/oauth/access_token'
    #     payload = {
    #         'client_id': settings.GH_CLIENT_ID,
    #         'client_secret': settings.GH_SECRET,
    #         'code': code,
    #         'redirect_uri': settings.GH_CALLBACK_URL,
    #     }
    #     headers = {'Accept': 'application/json'}
    #     response = requests.post(token_url, data=payload, headers=headers)
    #     access_token = response.json().get('access_token')
    #
    #     return Response({'access_token': access_token})
    # else:
    #     return Response({'error': 'Code not provided'}, status=400)