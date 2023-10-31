from django.core.management import BaseCommand

from one_big_thing.learning.models import User


class Command(BaseCommand):
    help = "users have recorded seven hours but not the end survey"

    def handle(self, *args, **kwargs):
        for user in User.objects.seven_hours_no_end_evaluation().values_list("email"):
            self.stdout.write(user.email)
