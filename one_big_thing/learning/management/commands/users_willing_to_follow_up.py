from django.core.management import BaseCommand

from one_big_thing.learning.models import SurveyResult


class Command(BaseCommand):
    help = "users that are willing to be emailed for a follow up"

    def handle(self, *args, **kwargs):
        for email, *_ in SurveyResult.objects.filter(
            data__contains={"willing-to-follow-up": "yes"},
        ).values_list("user__email"):
            self.stdout.write(email)
