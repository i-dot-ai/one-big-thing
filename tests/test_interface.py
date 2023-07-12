from one_big_thing.learning import interface, models

USER_DATA = {"email": "mr_interface_test@example.com", "password": "1-h4t3-p455w0rd-c0mpl3xity-53tt1ng5"}


def test_course_api():
    user, _ = models.User.objects.get_or_create(email=USER_DATA["email"])
    result = interface.api.course.create(data={"title": "Test title", "time_to_complete": "120"})
    assert result["title"] == "Test title", result["title"]
    assert result["time_to_complete"] == "120", result["time_to_complete"]


def test_completion_api():
    user, _ = models.User.objects.get_or_create(email=USER_DATA["email"])
    result = interface.api.course.create(data={"title": "Test title", "time_to_complete": "120"})
    assert result["title"] == "Test title", result["title"]
    assert result["time_to_complete"] == "120", result["time_to_complete"]

    completion_result = interface.api.completion.create(user_id=user.id, course_id=result["id"], user_to_add=user.id)

    completion = models.Completion.objects.get(pk=completion_result["completion_id"])
    assert completion.course.title == "Test title", completion.course.title
