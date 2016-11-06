from django.db.models.signals import post_save

import factory
import pytest

pytest.mark.unit


@pytest.mark.django_db
def test_meta_url_str(meta_url):
    assert meta_url.og_title == str(meta_url)
    meta_url.og_title = ''
    meta_url.save()
    meta_url.refresh_from_db()
    assert str(meta_url.created_at) == str(meta_url)


@pytest.mark.django_db
def test_meta_url_short_description(meta_url):
    assert len(meta_url.short_description) == 140


@pytest.mark.django_db
def test_share_title_display_with_title(share):
    assert share.title_display == share.title


@pytest.mark.django_db
def test_share_title_display_without_title(share):
    share.title = ''
    with factory.django.mute_signals(post_save):
        share.save()
    assert share.title_display == share.url
