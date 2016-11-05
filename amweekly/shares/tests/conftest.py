from amweekly.shares.tests.factories import MetaURLFactory, ShareFactory

import pytest


@pytest.fixture
def meta_url():
    return MetaURLFactory()


@pytest.fixture
def share():
    return ShareFactory()
