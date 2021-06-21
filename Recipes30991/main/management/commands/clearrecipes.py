from django.core.management.base import BaseCommand

from main.models import Recipe, Like


class Command(BaseCommand):
    help = 'Clears all the recipe info'

    def handle(self, *args, **options):
        obj = Recipe.objects
        if obj:
            obj.all().delete()
        obj2 = Like.objects
        if obj2:
            obj2.all().delete()
        self.stdout.write(self.style.SUCCESS('Recipes wiped out'))
