from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_save

from amweekly.shares.jobs import get_og_object, hydrate_share_meta_url, \
    CACHE_APP_ACCESS_TOKEN

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


@pytest.mark.slowtest
def test_get_og_object_caches_app_access_token():
    get_og_object('http://facebook.com')
    app_access_token = cache.get(CACHE_APP_ACCESS_TOKEN)
    assert app_access_token is not None


@pytest.mark.django_db
def test_hydrate_share_meta_url_invalid_share_id():
    invalid_id = factory.fuzzy.FuzzyInteger(9999, 99999)
    hydrate_share_meta_url(invalid_id.fuzz())
    assert True


@pytest.mark.django_db
def test_hydrate_share_meta_url_invalid_og_object(share, mocker):
    patched = mocker.patch('amweekly.shares.jobs.get_og_object')
    patched.return_value = {'id': None}
    with pytest.raises(Exception):
        hydrate_share_meta_url(share.id)


@pytest.mark.django_db
def test_hydrate_share_meta_url_sets_meta_url_from_og_object(share, mocker):
    patched = mocker.patch('amweekly.shares.jobs.get_og_object')
    expected = {
        'id': 'test_id',
        'title': 'test_title',
        'description': 'test_description',
        'type': 'test_type'}
    patched.return_value = expected
    hydrate_share_meta_url(share.id)
    share.refresh_from_db()
    assert expected == {
        'id': share.meta_url.og_id,
        'title': share.meta_url.og_title,
        'description': share.meta_url.og_description,
        'type': share.meta_url.og_type}


@pytest.mark.slowtest
@pytest.mark.django_db
def test_hydrate_share_meta_url(share):
    share.url = 'http://facebook.com'
    with factory.django.mute_signals(post_save):
        share.save()
    hydrate_share_meta_url(share.id)
    share.refresh_from_db()
    assert 'Facebook' in share.meta_url.og_title
