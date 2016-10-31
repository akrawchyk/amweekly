from amweekly.shares.tests.factories import MetaURLFactory, ShareFactory

import pytest


@pytest.mark.django_db
@pytest.fixture
def meta_url_factory():
    return MetaURLFactory()


@pytest.mark.django_db
@pytest.fixture
def share_factory():
    return ShareFactory()
