import json

from django.core.management import BaseCommand

from one_big_thing.api_serializers import DepartmentBreakdownSerializer
from one_big_thing.learning.api_views import get_learning_breakdown_data


class Command(BaseCommand):
    help = "Duplicate stats from API on department learning breakdowns"

    def handle(self, *args, **kwargs):
        groupings = get_learning_breakdown_data()
        output = DepartmentBreakdownSerializer(groupings, many=True)
        output_str = json.dumps(output.data)
        self.stdout.write(output_str)
