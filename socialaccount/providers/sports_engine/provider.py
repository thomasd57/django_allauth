import logging
from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider

from .utils import debug_save_data

class SportsEngineAccount(ProviderAccount):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

    def get_avatar_url(self):
        avatar_url =  self.account.extra_data.get('avatar_url')
        self.logger.debug('avatar_url=' + str(avatar_url))

    def to_str(self):
        dflt = super().to_str()
        s = next(
            value
            for value in (
                self.account.extra_data.get('name', None),
                self.account.extra_data.get('login', None),
                dflt
            )
            if value is not None
        )
        self.logger.debug('to_str=' + str(s))
        return s

class SportsEngineProvider(OAuth2Provider):
    id = 'sports_engine'
    name = 'SportsEngine'
    account_class = SportsEngineAccount
    package = 'socialaccount.providers.sports_engine'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

    def extract_uid(self, data):
        debug_save_data(data, 'extract_uid.json')
        id_ = str(data[0]['id'])
        self.logger.debug('extract_uid=' + id_)
        return id_

    def extract_common_fields(self, data):
        debug_save_data(data, 'extract_common_fields.json')
        data = data[0]
        email = data['email_addresses'][0]['address']
        fields = {
            'email'     : email,
            'username'  : email.split('@')[0],
            'name'      : data['first_name'] + ' ' + data['last_name'],
            'avatar_url': data.get('profile_image_url'),
        }
        self.logger.debug('extract_common_fields,email={}, username={}, name={}'.format(
            fields['email'], fields['username'], fields['name']))
        return fields

providers_classes = [SportsEngineProvider]
providers.registry.register(SportsEngineProvider)
