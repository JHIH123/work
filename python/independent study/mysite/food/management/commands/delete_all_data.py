from django.core.management.base import BaseCommand
from food.models import Place

class Command(BaseCommand):
    help = 'Delete all data from the Place model'

    def handle(self, *args, **kwargs):
        Place.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all data from the Place model'))
