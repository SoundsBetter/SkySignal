from allauth.account.adapter import DefaultAccountAdapter

from django.conf import settings

class AccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        key = emailconfirmation.key
        frontend_url = settings.ACCOUNT_VERIFICATION_DOMAIN
        return f"{frontend_url}/{key}/"