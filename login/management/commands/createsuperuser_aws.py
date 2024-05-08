from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.conf import settings
# https://github.com/codingforentrepreneurs/Guides/blob/master/all/elastic_beanstalk_django.md
class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="DigiCaddieSuper").exists():
            password = settings.SUPER_USER_PASSWORD
            User.objects.create_superuser("DigiCaddieSuper", "digicaddie@gmail.com", password)