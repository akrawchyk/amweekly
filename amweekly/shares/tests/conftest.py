from amweekly.shares.tests.factories import MetaURLFactory, ShareFactory

import pytest


@pytest.fixture
def meta_url_factory():
    return MetaURLFactory()


@pytest.fixture
def share_factory():
    return ShareFactory
