import yaml
from django.conf import settings

from one_big_thing.learning import models

with (settings.BASE_DIR / "special-courses.yaml").open() as f:
    special_courses_data = yaml.safe_load(f)


def get_special_course_information():
    courses = []
    for section in special_courses_data:
        course = models.Course.objects.filter(title=section["title"])
        if course:
            courses.append(course.first())
    return courses


def get_special_course_ids():
    course_ids = []
    for section in special_courses_data:
        course = models.Course.objects.filter(title=section["title"])
        if course:
            course_ids.append(course.first().id)
    return course_ids
