import json

from django.core.management import BaseCommand

from one_big_thing.api_serializers import DateJoinedSerializer
from one_big_thing.learning.api_views import get_signups_by_date


class Command(BaseCommand):
    help = "Duplicate stats from API on signups"

    def handle(self, *args, **kwargs):
        signups = get_signups_by_date()
        output = DateJoinedSerializer(signups, many=True)
        output_str = json.dumps(output.data)
        self.stdout.write(output_str)
