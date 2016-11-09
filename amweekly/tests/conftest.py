from amweekly.shares.tests.factories import ShareFactory

import pytest


@pytest.fixture
def share():
    return ShareFactory()
