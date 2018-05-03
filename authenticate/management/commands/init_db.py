import os.path
import environ

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings

class Command(BaseCommand):
    help = "create superuser and social accounts from .env file"
    env = environ.Env(
            SUPERUSER_USERID = (str, 'admin'),
            SUPERUSER_EMAIL  = (str, 'admin@example.com'),
            SUPERUSER_PASSWORD = (str, 'adminadmin'),
        )

    def add_arguments(self, parser):
        parser.add_argument('--env_file', help = 'Environment file', default = 'env.env')

    def handle(self, *args, **options):
        self.read_env(options['env_file'])
        self.create_superuser()

    def create_superuser(self):
        User.objects.create_superuser(
                self.env('SUPERUSER_USERID'),
                self.env('SUPERUSER_EMAIL'),
                self.env('SUPERUSER_PASSWORD')
        )

    def read_env(self, env_file):
        env_file = os.path.join(settings.BASE_DIR, env_file)
        if os.path.isfile(env_file):
            environ.Env.read_env(env_file)

