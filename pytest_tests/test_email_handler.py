import pytest

from one_big_thing.learning.models import Department, User


@pytest.mark.django_db
def test_send_email_learning_record(client, mailoutbox):
    email = "jim@example.com"
    sign_up_page = client.post("/", {"email": email})
    assert sign_up_page.status_code == 302

    user = User.objects.get(email=email)
    user.has_completed_pre_survey = True
    user.verified = True
    user.grade = "GRADE7"
    user.profession = "ANALYSIS"
    user.department = Department.objects.get(code="cabinet-office")
    user.save()

    magic_link_page = client.get(mailoutbox[-1].body.split("\n")[3])
    assert magic_link_page.status_code == 302

    new_person_email = "a_different_email@example.com"
    page = client.post("/send-learning-record/", {"email": new_person_email})
    assert f"Your learning record has successfully been sent to {new_person_email}" in page.content.decode()
    assert new_person_email in mailoutbox[-1].to