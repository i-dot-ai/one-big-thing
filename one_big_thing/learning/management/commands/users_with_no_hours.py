from django.core.management import BaseCommand

from one_big_thing.learning.models import User


class Command(BaseCommand):
    help = "users have recorded no learning"

    def handle(self, *args, **kwargs):
        for user in User.objects.no_learning_recorded():
            self.stdout.write(user.email)
