from django.core.exceptions import ImproperlyConfigured

import httpretty
import pytest

from amweekly.shares.jobs import get_facebook_access_token, FACEBOOK_OAUTH_URL

pytest.mark.integration


def test_unconfigured_facebook_client_id(settings):
    settings.FACEBOOK_CLIENT_ID = ''
    with pytest.raises(ImproperlyConfigured):
        get_facebook_access_token()


def test_unconfigured_facebook_client_secret(settings):
    settings.FACEBOOK_CLIENT_SECRET = ''
    with pytest.raises(ImproperlyConfigured):
        get_facebook_access_token()


@pytest.mark.httpretty
def test_get_facebook_access_token_net_error():
    httpretty.register_uri(
        httpretty.GET,
        FACEBOOK_OAUTH_URL,
        body='param=mock_token',
        status=500)

    with pytest.raises(ImproperlyConfigured):
        get_facebook_access_token()


@pytest.mark.httpretty
def test_get_facebook_access_token():
    httpretty.register_uri(
        httpretty.GET,
        FACEBOOK_OAUTH_URL,
        body='param=mock_token')

    token = get_facebook_access_token()
    assert token == 'mock_token'
