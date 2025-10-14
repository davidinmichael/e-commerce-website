import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from business.models import Category

load_dotenv()

categories = [
    "Phones",
    "Computers",
    "Games",
    "AirPods",
    "Smart Watch"
]


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for category in categories:
            Category.objects.create(
                name=category, description=f"A category about {category}"
            )
        self.stdout.write(self.style.SUCCESS("Categories Addded!"))
