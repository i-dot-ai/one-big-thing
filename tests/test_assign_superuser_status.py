from datetime import datetime
from io import StringIO

from django.core.management import call_command

from one_big_thing.learning.models import User


def test_assign_superuser_status_happy_path():
    """we create a new user, initially they are not a superuser,
    we then make them one and check that a OTP link is returned
    """
    email = "diana@co.gov.uk"
    user = User.objects.create_user(email="diana@co.gov.uk")
    assert user.is_superuser is False

    stdout = StringIO()
    call_command("assign_superuser_status", "--email", email, stdout=stdout)
    lines = stdout.getvalue().split("\n")
    assert lines[0].startswith("otpauth://totp/OneBigThing")
    user.refresh_from_db()
    assert user.is_superuser is True
