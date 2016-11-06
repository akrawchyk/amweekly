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
def test_share_title_display(share, meta_url):
    share.meta_url = meta_url
    share.save()
    assert share.title_display == share.title
    share.title = ''
    share.save()
    assert share.title_display == share.url
