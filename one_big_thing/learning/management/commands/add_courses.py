from django.core.management import BaseCommand

from one_big_thing.learning import choices, models

courses = (
    {
        "link": "https://learn.civilservice.gov.uk/courses/GyZgKWc0Tz6ZIfvDSiuO1Q",
        "title": "Data quality",
        "duration": "80",
        "learning_type": choices.CourseType.LINK.name,
    },
    {
        "link": "https://learn.civilservice.gov.uk/courses/2PAR3NQyT-GOg5-7bVZaog",
        "title": "Data visualisation",
        "duration": "60",
        "learning_type": choices.CourseType.LINK.name,
    },
    {
        "link": "https://learn.civilservice.gov.uk/courses/BfBwomNDSEGgpf9b16RJsg",
        "title": "Data visualisation e-learning",
        "duration": "30",
        "learning_type": choices.CourseType.LINK.name,
    },
    {
        "link": "https://learn.civilservice.gov.uk/courses/1bzxx1maReOyvnxFIYOP1g",
        "title": "Security and data protection",
        "duration": "95",
        "learning_type": choices.CourseType.LINK.name,
    },
    {
        "link": "https://learn.civilservice.gov.uk/courses/s5y7_eboT4iIuz2sUTB-CQ",
        "title": "Government security classification policy",
        "duration": "30",
        "learning_type": choices.CourseType.LINK.name,
    },
)


class Command(BaseCommand):
    help = "Add fake courses"

    def handle(self, *args, **kwargs):
        for course in courses:
            new_course = models.Course()
            new_course.title = course["title"]
            new_course.link = course["link"]
            new_course.time_to_complete = course["duration"]
            new_course.learning_type = course["learning_type"]
            new_course.save()
