from datetime import datetime

import pytest
import pytz

from one_big_thing.learning.models import User

UTC = pytz.timezone('UTC')


@pytest.fixture
def create_user():
    def _create_user(email, date_joined_iso):
        date_joined = UTC.localize(datetime.fromisoformat(date_joined_iso))
        user = User.objects.create_user(email=email, date_joined=date_joined)
        return user

    return _create_user

@pytest.fixture
def alice(create_user):
    return create_user("alice@co.gov.uk", "2000-01-01")

@pytest.fixture
def bob(create_user):
    return create_user("bob@co.gov.uk", "2000-01-01")

@pytest.fixture
def chris(create_user):
    return create_user("chris@co.gov.uk", "2000-01-02")
