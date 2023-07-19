import yaml
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Add special courses, e.g. manager meeting"

    def handle(self, *args, **kwargs):
        with (settings.BASE_DIR / "special-courses.yaml").open() as f:
            special_courses = yaml.safe_load(f)
