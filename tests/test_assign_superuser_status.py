from io import StringIO

from django.core.management import call_command

from one_big_thing.learning.models import User


def test_assign_superuser_status_happy_path():
    """we create a new user, initially they are not a superuser,
    we then make them one and check that:
    1. a TOTP link is returned
    2. the user now has a password
    3. the user is now a staff and superuser
    """
    email, password = "diana@co.gov.uk", "P4ssw0rd!"
    user = User.objects.create_user(email="diana@co.gov.uk")
    assert user.is_superuser is False
    assert user.is_staff is False

    stdout = StringIO()

    call_command("assign_superuser_status", "--email", email, "--password", password, stdout=stdout)

    lines = stdout.getvalue().split("\n")
    # 1. do we get the totp link?
    assert lines[0].startswith("otpauth://totp/OneBigThing")

    # fetch updated user state
    user.refresh_from_db()

    # 2. has the password been set correctly?
    assert user.check_password(password), user.password

    # 3. is the user a staff and superuser?
    assert user.is_superuser is True
    assert user.is_staff is True
