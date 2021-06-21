from django.core.management.base import BaseCommand

from main.models import Comment


class Command(BaseCommand):
    help = 'Clears all the comment info'

    def handle(self, *args, **options):
        obj = Comment.objects
        if obj:
            obj.all().delete()
        self.stdout.write(self.style.SUCCESS('Comments wiped out'))
