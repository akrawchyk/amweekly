from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured

import pytest

from amweekly.shares.jobs import get_og_object, hydrate_share_meta_url, \
    CACHE_APP_ACCESS_TOKEN

pytest.mark.integration


def test_unconfigured_facebook_client_id(settings):
    settings.FACEBOOK_CLIENT_ID = ''
    with pytest.raises(ImproperlyConfigured):
        get_og_object(None)


def test_unconfigured_facebook_client_secret(settings):
    settings.FACEBOOK_CLIENT_SECRET = ''
    with pytest.raises(ImproperlyConfigured):
        get_og_object(None)


def test_get_og_object_caches_app_access_token():
    get_og_object('http://facebook.com')
    app_access_token = cache.get(CACHE_APP_ACCESS_TOKEN)
    assert app_access_token is not None


@pytest.mark.django_db
def test_hydrate_share_meta_url(share_factory):
    share = share_factory(url='http://facebook.com')
    share.save()
    hydrate_share_meta_url(share.id)
    meta_url = share.meta_url
    assert 'Facebook' in meta_url['og_title']
