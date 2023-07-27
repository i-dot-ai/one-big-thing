import yaml
from django.conf import settings
from django.core.management import BaseCommand

from one_big_thing.learning import models


class Command(BaseCommand):
    help = "Add special courses, e.g. manager meeting"

    def handle(self, *args, **kwargs):
        with (settings.BASE_DIR / "special-courses.yaml").open() as f:
            special_courses = yaml.safe_load(f)
            for special_course in special_courses:
                course, _ = models.Course.objects.get_or_create(
                    title=special_course["title"],
                    link=special_course["link"],
                    learning_type=special_course["learning_type"],
                    time_to_complete=special_course["time_to_complete"],
                    is_special_course=True,
                )
                course.save()
