from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username="vivekraj").exists():
            User.objects.create_superuser("vivekraj", "raj.vivek.151297@gmail.com", "bsnl3g3g")