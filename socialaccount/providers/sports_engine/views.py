import requests
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)
from .provider import SportsEngineProvider

class SportsEngineOAuth2Adapter(OAuth2Adapter):
    provider_id = SportsEngineProvider.id
    access_token_url = 'https://user.sportngin.com/oauth/token'
    authorize_url = 'https://user.sportngin.com/oauth/authorize'
    profile_url = ''

    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': 'Bearer {0}'.format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request,
                                                             extra_data)

oauth2_login = OAuth2LoginView.adapter_view(SportsEngineOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(SportsEngineOAuth2Adapter)
