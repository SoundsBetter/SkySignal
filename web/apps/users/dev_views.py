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