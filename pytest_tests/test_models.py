import pytest

from one_big_thing.learning import models
from one_big_thing.learning.models import Department, SurveyResult


@pytest.mark.django_db
def test_model_fields():
    course = models.Course(time_to_complete=120, title="Test course")
    course.save()

    user, _ = models.User.objects.get_or_create(email="mrs.tiggywinkle@cabinetoffice.gov.uk")
    user.save()

    learning = models.Learning(title=course.title, user=user, time_to_complete=course.time_to_complete, course=course)
    learning.save()

    assert learning.course == course
    assert learning.course.title == "Test course"
    assert learning.course.time_to_complete == 120
    course.title = "New course title"
    course.save()
    assert course.title == "New course title"


@pytest.mark.django_db
def test_user_save():
    new_email1 = "New_User1@example.org"
    new_email2 = "New_User2@Example.com"
    new_user1, _ = models.User.objects.update_or_create(email=new_email1)
    new_user2, _ = models.User.objects.update_or_create(email=new_email2)
    assert new_user1.email == "new_user1@example.org", new_user1.email
    assert new_user2.email == "new_user2@example.com", new_user2.email


@pytest.mark.django_db
def test_survey_results(create_user):
    alice = create_user(email="alice@example.com")
    SurveyResult.objects.create(
        user=alice,
        survey_type="pre",
        page_number=1,
    )
    SurveyResult.objects.create(
        user=alice,
        survey_type="pre",
        page_number=2,
    )
    SurveyResult.objects.create(
        user=alice,
        survey_type="post",
        page_number=3,
    )
    SurveyResult.objects.create(
        user=alice,
        survey_type="working",
        page_number=4,
    )
    SurveyResult.objects.create(
        user=alice,
        survey_type="practitioner",
        page_number=5,
    )

    assert len(alice.pre_survey_results) == 2
    assert [result.page_number for result in alice.pre_survey_results] == [1, 2]

    assert len(alice.post_survey_results) == 3
    assert [result.page_number for result in alice.post_survey_results] == [3, 4, 5]


def test_determine_competency_levels():
    input1 = ["", "not-confident", "confident"]
    input2 = ["not-confident", "confident", "very-confident"]
    input3 = ["", "very-confident", "very-confident"]
    input4 = ["not-confident", "", ""]
    input5 = ["", "", ""]
    expected1 = "working"
    expected2 = "working"
    expected3 = "practitioner"
    expected4 = "awareness"
    expected5 = None
    actual1 = models.determine_competency_levels(input1)
    actual2 = models.determine_competency_levels(input2)
    actual3 = models.determine_competency_levels(input3)
    actual4 = models.determine_competency_levels(input4)
    actual5 = models.determine_competency_levels(input5)
    assert expected1 == actual1, actual1
    assert expected2 == actual2, actual2
    assert expected3 == actual3, actual3
    assert expected4 == actual4, actual4
    assert expected5 == actual5, actual5


@pytest.mark.django_db
def test_completed_personal_details():
    user = models.User(email="jane@example.com")
    user.save()
    assert not user.completed_personal_details, user.completed_personal_details
    user.grade = "HEO"
    user.save()
    assert not user.completed_personal_details, user.completed_personal_details
    user.profession = "ANALYSIS"
    user.department = Department.objects.get(code="cabinet-office")
    user.save()
    assert user.completed_personal_details, user.completed_personal_details
    user.delete()


@pytest.mark.django_db
def test_no_learning_recorded(alice, faye, george):
    """
    * alice has spent 60 minutes on one course
    * faye has recorded zero minutes on two courses
    * george has done no courses
    """
    users = models.User.objects.no_learning_recorded().values_list("email")
    assert list(users) == [("faye@co.gov.uk",), ("george@co.gov.uk",)]


@pytest.mark.django_db
def test_seven_hours_no_end_evaluation(bob, hannah, isaac):
    """
    * alice hasnt done seven hours and hasnt completed the survey
    * hannah has done seven hours and hasn completed the survey
    * isaac has done more than seven hours but hasnt completed the survey
    """
    users = models.User.objects.seven_hours_no_end_evaluation().values_list("email")
    assert list(users) == [("isaac@co.gov.uk",)]
