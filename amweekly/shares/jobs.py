import logging

from django.core.cache import cache
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import facebook

from amweekly.shares.models import MetaURL, Share

logger = logging.getLogger(__name__)

CACHE_APP_ACCESS_TOKEN = 'shares.jobs.app_access_token'

"""
Expected Graph API Response:
{
    "og_object": {
        "id": "1015012577744568"
        "type": "fitness.course",
        "url": "http://www.example.com/route3875037.html",
        "description": "New personal best!",
        "title": "My Run",
        "image": "http://www.example.com/screencap.png”
    }
}
"""


def get_og_object(id):
    if settings.FACEBOOK_APP_ID is '' or \
       settings.FACEBOOK_APP_SECRET is '':
        raise ImproperlyConfigured(
            'FACEBOOK_APP_ID or FACEBOOK_APP_SECRET not configured')

    app_access_token = cache.get(CACHE_APP_ACCESS_TOKEN)

    if app_access_token is None:
        app_access_token = facebook.GraphAPI().get_app_access_token(
            settings.FACEBOOK_APP_ID,
            settings.FACEBOOK_APP_SECRET)
        cache.set(CACHE_APP_ACCESS_TOKEN, app_access_token, 3600)

    graph = facebook.GraphAPI(app_access_token)

    if id is not None:
        og = graph.get_object(id=id)
    else:
        raise Exception('Required id argument')

    og_object = None

    if 'og_object' in og:
        og_object = og['og_object']
    else:
        logger.error(f'No Open Graph object found for {id}')

    return og_object


def hydrate_share_meta_url(share_id):
    try:
        share = Share.objects.get(pk=share_id)
        og_object = get_og_object(share.url)

        if og_object['id'] is None:
            raise Exception(
                f'No Open Graph object returned for Share {share_id}')

        meta_url, created = MetaURL.objects.get_or_create(
            og_id=og_object['id'])

        keys = ('title', 'description', 'type', 'id')
        for k in keys:
            if k in og_object:
                setattr(meta_url, f'og_{k}', og_object[k])

        meta_url.share_set.add(share)
        meta_url.save()
    except Share.DoesNotExist:
        logger.error(f'Share with id {share_id} does not exist.')
