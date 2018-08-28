import json, sys, pdb
import logging
import requests
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)
from .provider import SportsEngineProvider
from .utils import debug_save_data

class SportsEngineOAuth2Adapter(OAuth2Adapter):
    provider_id = SportsEngineProvider.id
    access_token_url = 'https://user.sportngin.com/oauth/token'
    authorize_url = 'https://user.sportngin.com/oauth/authorize'
    # profile_url = 'http://user.sportngin.com/oauth/me'
    profile_url = 'https://api.sportngin.com/user_personas'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(self.profile_url,
                headers = { 'NGIN-API-VERSION' : '0.1',
                            'Authorization': 'Bearer ' + str(token)}) 
        extra_data = resp.json()
        debug_save_data(extra_data, 'complete_login.json')
        data = self.get_provider().sociallogin_from_response(request,
                                                             extra_data)
        return data

    def get_email(self, token):
        resp = requests.get(self.profile_url,
                headers = { 'NGIN-API-VERSION' : '0.1',
                            'Authorization': 'Bearer ' + str(token)}) 
        data = resp.json()
        email = data[0]['email_addresses'][0]['address']
        return email

oauth2_login = OAuth2LoginView.adapter_view(SportsEngineOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(SportsEngineOAuth2Adapter)
