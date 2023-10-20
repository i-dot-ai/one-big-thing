import pytest

from one_big_thing.learning import interface, models

USER_DATA = {"email": "mr_interface_test@example.com", "password": "1-h4t3-p455w0rd-c0mpl3xity-53tt1ng5"}


@pytest.mark.django_db
def test_course_api():
    result = interface.api.course.create(data={"title": "Test title", "time_to_complete": "120"})
    assert result["title"] == "Test title", result["title"]
    assert result["time_to_complete"] == "120", result["time_to_complete"]


@pytest.mark.django_db
def test_learning_api(alice):
    result = interface.api.course.create(data={"title": "Test title", "time_to_complete": "120"})
    assert result["title"] == "Test title", result["title"]
    assert result["time_to_complete"] == "120", result["time_to_complete"]

    learning_result = interface.api.learning.create(
        user_id=alice.id,
        user_to_add=alice.id,
        data={"title": "Test title", "time_to_complete": "120"},
        course_id=result["id"],
    )

    learning = models.Learning.objects.get(pk=learning_result["learning_id"])
    assert learning.course.title == "Test title", learning.course.title
