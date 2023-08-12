import yaml
from django.conf import settings

from one_big_thing.learning import models

with (settings.BASE_DIR / "special-courses.yaml").open() as f:
    special_courses_data = yaml.safe_load(f)


practitioner_course_title = "Data masterclass (Level 3 - Practitioner)"
working_course_title = "Working with data (Level 2 - Working)"
awareness_course_title = "Understanding data (Level 1 - Awareness)"


competency_level_courses = {
    "beginner": awareness_course_title,
    "intermediate": working_course_title,
    "expert": practitioner_course_title,
}


def get_special_course_ids():
    course_ids = []
    for section in special_courses_data:
        course = models.Course.objects.filter(title=section["title"])
        if course:
            course_ids.append(course.first().id)
    return course_ids


def get_special_course_information(course_title):
    special_course = models.Course.objects.filter(title=course_title).first()
    return special_course
