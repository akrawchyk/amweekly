from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_save

from amweekly.shares.jobs import get_og_object, hydrate_share_meta_url, \
    CACHE_APP_ACCESS_TOKEN
from amweekly.shares.tests.factories import ShareFactory


import factory
import pytest

pytest.mark.integration


def test_unconfigured_facebook_client_id(settings):
    settings.FACEBOOK_APP_ID = ''
    with pytest.raises(ImproperlyConfigured):
        get_og_object(None)


def test_unconfigured_facebook_client_secret(settings):
    settings.FACEBOOK_APP_SECRET = ''
    with pytest.raises(ImproperlyConfigured):
        get_og_object(None)


def test_get_og_object_caches_app_access_token():
    get_og_object('http://facebook.com')
    app_access_token = cache.get(CACHE_APP_ACCESS_TOKEN)
    assert app_access_token is not None


@pytest.mark.django_db
def test_hydrate_share_meta_url():
    # TODO should be able to put this as a decorator on the factory...
    with factory.django.mute_signals(post_save):
        share = ShareFactory(url='http://facebook.com')
        share.save()
        hydrate_share_meta_url(share.id)
        share = ShareFactory(url='http://facebook.com')
        meta_url = share.meta_url
        assert 'Facebook' in meta_url.og_title
