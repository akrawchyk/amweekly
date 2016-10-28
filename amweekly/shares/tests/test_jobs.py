from django.core.exceptions import ImproperlyConfigured

import httpretty
import pytest

from amweekly.shares.jobs import get_facebook_access_token, FACEBOOK_OAUTH_URL

pytest.mark.integration


def test_misconfigured_facebook_client_id(settings):
    settings.FACEBOOK_CLIENT_ID = ''

    try:
        get_facebook_access_token()
        assert False
    except ImproperlyConfigured:
        pass


def test_misconfigured_facebook_client_secret(settings):
    settings.FACEBOOK_CLIENT_SECRET = ''

    try:
        get_facebook_access_token()
        assert False
    except ImproperlyConfigured:
        pass


@pytest.mark.httpretty
def test_get_facebook_access_token(settings):
    settings.CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

    httpretty.register_uri(
        httpretty.GET,
        FACEBOOK_OAUTH_URL,
        body='param=mock_token'
    )

    token = get_facebook_access_token()
    assert token == 'mock_token'
