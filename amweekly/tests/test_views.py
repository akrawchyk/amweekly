from amweekly.views import HomePageView

import pytest

pytest.mark.integration


def test_home_page_view(rf):
    request = rf.get('/')
    response = HomePageView.as_view()(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_home_page_view_shares(rf, share):
    request = rf.get('/')
    response = HomePageView.as_view()(request)
    assert len(response.context_data['shares']) == 1
