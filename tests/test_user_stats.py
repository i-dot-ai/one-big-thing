from datetime import datetime
from io import StringIO

from django.core.management import call_command
from one_big_thing.learning.models import User


def test_user_stats():
    """we create 3 users, alice and bob were both joined on the same day
    chris joined 1 day after, we expect to see this is the standard out"""

    for email, iso in [
        ("alice@co.gov.uk", "2000-01-01"),
        ("bob@co.gov.uk", "2000-01-01"),
        ("charlie@co.gov.uk", "2000-01-02"),
    ]:
        User.objects.create_user(email=email, date_joined=datetime.fromisoformat(iso))

    stdout = StringIO()
    call_command("user_stats", stdout=stdout)
    lines = stdout.getvalue().split("\n")

    assert "2000-01-01, 2" in lines
    assert "2000-01-02, 1" in lines
