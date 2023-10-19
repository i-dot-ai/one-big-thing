from django.core.management import BaseCommand

from one_big_thing.learning.models import User


class Command(BaseCommand):
    help = "users that are willing to be emailed for a follow up"

    def handle(self, *args, **kwargs):
        for email, *_ in User.objects.filter(
            surveyresult__data__contains={"willing-to-follow-up": "yes"},
        ).values_list("email"):
            self.stdout.write(email)
