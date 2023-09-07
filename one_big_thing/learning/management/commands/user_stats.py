from django.core.management import BaseCommand
from django.db.models import Count
from django.db.models.functions import TruncDay

from one_big_thing.learning.models import User


class Command(BaseCommand):
    help = "Count number of new users per day"

    def handle(self, *args, **kwargs):
        members_per_day = (
            User.objects.values(day=TruncDay("date_joined")).annotate(count=Count("date_joined")).order_by("day")
        )

        self.stdout.write("date, count")
        for record in members_per_day:
            day = record["day"].date()
            count = record["count"]
            self.stdout.write(f"{day}, {count}")
