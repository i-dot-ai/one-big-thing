import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_users_with_no_hours(create_user, mailoutbox):
    """we create 3 users:
    1. alice has recorded zero learning hours in one course
    2. bob has recorded no learning
    3. claire has completed 100 minutes of learning

    we expect alice and bob to receive an email
    """

    create_user(
        email="alice@example.com",
        times_to_complete=[0],
    )
    create_user(
        email="bob@example.com",
        times_to_complete=[],
    )
    create_user(
        email="claire@example.com",
        times_to_complete=[100],
    )

    call_command("users_with_no_hours")

    assert len(mailoutbox) == 2
    assert {to for mail in mailoutbox for to in mail.to} == {"alice@example.com", "bob@example.com"}

    with open("one_big_thing/templates/email/recorded-your-learning.txt") as f:
        expected_text = f.read()
    assert mailoutbox[0].body == expected_text


@pytest.mark.django_db
def test_users_with_seven_hours_no_survey(create_user, mailoutbox):
    """we create 3 users:
    * alice has done one hour and hasn't completed the survey
    * bob has done more than seven hours and hasn't completed the survey
    * claire has done more than seven hours and has completed the survey

    we expect bob to receive an email
    """

    create_user(
        email="alice@example.com",
        times_to_complete=[60],
        has_completed_post_survey=False,
    )
    create_user(
        email="bob@example.com",
        times_to_complete=[60 * 7 + 1],
    )
    create_user(email="claire@example.com", times_to_complete=[60 * 7 + 1], has_completed_post_survey=True)

    call_command("users_with_seven_hours_no_survey")

    assert len(mailoutbox) == 1
    assert {to for mail in mailoutbox for to in mail.to} == {
        "bob@example.com",
    }

    with open("one_big_thing/templates/email/provide-feedback.txt") as f:
        expected_text = f.read()
    assert mailoutbox[0].body == expected_text
