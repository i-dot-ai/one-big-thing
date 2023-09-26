import random

from django.core.management import BaseCommand

from one_big_thing.learning import models, departments, choices


TEST_USER_PASSWORD = "dummy-user-password"


class Command(BaseCommand):
    help = "Add lots of users and related learning records courses, e.g. manager meeting"

    def handle(self, *args, **kwargs):
        for i in range(1, 10000):
            _ = _add_user(i)


def _add_user(unique_id=random.randint(0, 2000)):
    user, _ = models.User.objects.get_or_create(
        email=f"test_{unique_id}@example.com",
        is_api_user=False,
        department=departments.department_tuples[random.randint(0, len(departments.department_tuples) - 1)][0],
        grade=choices.Grade.labels[random.randint(0, len(choices.Grade.labels) - 1)],
        profession=choices.Profession.labels[random.randint(0, len(choices.Profession.labels) - 1)],
        has_completed_post_survey=bool(random.choice([True, False])),
        has_completed_pre_survey=bool(random.choice([True, False])),
    )
    user.set_password(TEST_USER_PASSWORD)
    user.save()
    for i in range(0, 4):
        learning = models.Learning.objects.create(
            title=f"test learning {unique_id}",
            time_to_complete=random.randint(10, 120),
            user_id=user.id,
        )
        learning.save()
    return user
