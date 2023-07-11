from one_big_thing.learning import models


def test_model_fields():
    course = models.Course(time_to_complete=120, title="Test course")
    course.save()

    user, _ = models.User.objects.get_or_create(email="mrs.tiggywinkle@cabinetoffice.gov.uk")
    user.save()

    completion = models.Completion(course=course, user=user)
    completion.save()

    assert completion.course == course
    assert completion.course.title == "Test course"
    assert completion.course.time_to_complete == 120
    course.title = "New course title"
    course.save()
    assert course.title == "New course title"


def test_user_save():
    new_email1 = "New_User1@example.org"
    new_email2 = "New_User2@Example.com"
    new_user1, _ = models.User.objects.update_or_create(email=new_email1)
    new_user2, _ = models.User.objects.update_or_create(email=new_email2)
    assert new_user1.email == "new_user1@example.org", new_user1.email
    assert new_user2.email == "new_user2@example.com", new_user2.email
