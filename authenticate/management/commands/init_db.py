import os.path
import environ

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

class Command(BaseCommand):
    help = "create superuser and social accounts from .env file"
    env = environ.Env(
            SUPERUSER_USERID = (str, 'admin'),
            SUPERUSER_EMAIL  = (str, 'admin@example.com'),
            SUPERUSER_PASSWORD = (str, 'adminadmin'),
            DOMAIN_NAME = (str, settings.DOMAIN_NAME),
            COMPANY_NAME = (str, settings.COMPANY_NAME),

            GOOGLE_CLIENT_ID = (str, ''),
            GOOGLE_SECRET    = (str, ''),
            GITHUB_CLIENT_ID = (str, ''),
            GITHUB_SECRET    = (str, ''),
            FACEBOOK_CLIENT_ID = (str, ''),
            FACEBOOK_SECRET    = (str, ''),
            SPORTS_ENGINE_CLIENT_ID = (str, ''),
            SPORTS_ENGINE_SECRET    = (str, ''),
        )

    def add_arguments(self, parser):
        parser.add_argument('--env_file', help = 'Environment file', default = 'secrets.env')

    def handle(self, *args, **options):
        self.read_env(options['env_file'])
        self.create_superuser()
        self.create_site()
        for provider in ('GITHUB', 'FACEBOOK', 'GOOGLE', 'SPORTS_ENGINE'):
            if len(self.env(provider + '_CLIENT_ID')):
                self.create_social_account(provider.capitalize(), 
                            self.env(provider + '_CLIENT_ID'), 
                            self.env(provider + '_SECRET'))


    def create_superuser(self):
        User.objects.create_superuser(
                self.env('SUPERUSER_USERID'),
                self.env('SUPERUSER_EMAIL'),
                self.env('SUPERUSER_PASSWORD')
        )
        print('Created superuser', self.env('SUPERUSER_USERID'))

    def read_env(self, env_file):
        env_file = os.path.join(settings.BASE_DIR, env_file)
        if os.path.isfile(env_file):
            environ.Env.read_env(env_file)

    def create_social_account(self, name, client_id, secret):
        app = SocialApp.objects.create(provider = name.lower(), name = name, client_id = client_id, secret = secret)
        app.sites.add(Site.objects.get_current())
        app.save()
        print('Create social account', name)

    def create_site(self):
        site = Site.objects.get_current()
        site.domain = self.env('DOMAIN_NAME')
        site.name = self.env('COMPANY_NAME')
        site.save()
        print('Created site', site.domain)
