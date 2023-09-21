import random

import pytest

from one_big_thing.learning import choices, departments, models

TEST_USER_EMAIL = "test_pytest_user@example.com"
TEST_USER_PASSWORD = "test-api-password"


@pytest.fixture
def add_user():
    def _add_user(unique_id=random.randint(0, 2000)):
        user, _ = models.User.objects.get_or_create(
            email=f"test_{unique_id}@example.com",
            is_api_user=False,
            department=departments.department_tuples[random.randint(0, len(departments.department_tuples) - 1)][0],
            grade=choices.Grade.labels[random.randint(0, len(choices.Grade.labels) - 1)],
            profession=choices.Profession.labels[random.randint(0, len(choices.Profession.labels) - 1)],
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

    return _add_user
