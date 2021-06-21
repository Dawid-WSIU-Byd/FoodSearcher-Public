from django.core.management.base import BaseCommand

from main.models import Like, Recipe


class Command(BaseCommand):
    help = 'Clears all the like info'

    def handle(self, *args, **options):
        obj = Like.objects
        if obj:
            obj.all().delete()
        obj2 = Recipe.objects
        if obj2:
            for CurrentRecipe in obj2.all():
                CurrentRecipe.Likes = 0
                CurrentRecipe.save()
        self.stdout.write(self.style.SUCCESS('Likes wiped out'))
