from collections import defaultdict

from django.core.management import BaseCommand

from one_big_thing.learning.models import User


class Command(BaseCommand):
    help = "Count email domains per department"

    def handle(self, *args, **kwargs):
        counter = defaultdict(int)
        for user in User.objects.all():
            counter[(user.email_domain, user.department)] += 1

        self.stdout.write("domain, department, count")
        for (domain, department), count in counter.items():
            self.stdout.write(f"{domain}, {department}, {count}")
