from io import StringIO

import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_user_stats(alice, bob, chris):
    """we create 3 users, alice and bob both joined on the same day
    chris joined 1 day after, we expect to see this is the standard output
    """

    stdout = StringIO()
    call_command("user_stats", stdout=stdout)
    lines = stdout.getvalue().split("\n")

    assert "2000-01-01, 2" in lines
    assert "2000-01-02, 1" in lines
