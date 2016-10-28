import logging

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured

import facebook
import requests

from amweekly.shares.models import MetaURL, Share

logger = logging.getLogger(__name__)


FACEBOOK_OAUTH_URL = 'https://graph.facebook.com/oauth/access_token'


def get_facebook_access_token():
    if settings.FACEBOOK_CLIENT_ID is '' or \
       settings.FACEBOOK_CLIENT_SECRET is '':
        raise ImproperlyConfigured(
            'FACEBOOK_CLIENT_ID or FACEBOOK_CLIENT_SECRET not configured')

    facebook_access_token = cache.get('facebook_access_token')
    if facebook_access_token is None:
        logger.info('Requesting access token from Facebook')

        try:
            access_token_request = requests.get(FACEBOOK_OAUTH_URL, params={
                'client_id': settings.FACEBOOK_CLIENT_ID,
                'client_secret': settings.FACEBOOK_CLIENT_SECRET,
                'grant_type': 'client_credentials'
            })
            access_token_request.raise_for_status()
            facebook_access_token = access_token_request.text.split('=')[1]
            cache.set('facebook_access_token', facebook_access_token, 3600)
            logger.info('Facebook access token retrieved successfully')
        except requests.exceptions.HTTPError as e:
            raise ImproperlyConfigured(
                'Unable to retrieve Facebook access token: {}'.format(str(e)))

    return facebook_access_token


def get_og_object(lookup):
    """
    Expected Graph API Response
        {
        "og_object": {
            "id": "10150192219203164",
            "title": "https://developers.facebook.com/tools/explorer/",
            "type": "website",
            "updated_time": "2016-08-18T06:55:10+0000"
        },
        "share": {
            "comment_count": 4,
            "share_count": 2572
        },
        "id": "https://developers.facebook.com/tools/explorer/"
        }
    """
    facebook_access_token = get_facebook_access_token()
    graph = facebook.GraphAPI(facebook_access_token)
    og = graph.get_object(lookup)
    og_url = og['id']  # url as recognized by the open graph
    og_object = None
    if og_url is not None:
        if 'og_object' in og:
            og_object = og['og_object']
    return (og_url, og_object)


def refresh_share_meta_url(share_id):
    try:
        share = Share.objects.get(pk=share_id)
        og_url, og_object = get_og_object(share.url)
        meta_url, created = MetaURL.objects.get_or_create(og_url=og_url)

        refresh_meta_url(meta_url.id)
    except Share.DoesNotExist:
        logger.error('Share with id {} does not exist.'.format(share_id))


def refresh_meta_url(meta_url_id):
    try:
        meta_url = MetaURL.objects.get(pk=meta_url_id)
        og_url, og_object = get_og_object(meta_url.og_url)

        if og_object is not None:
            for k, v in og_object.items():
                if k == 'title':
                    meta_url.og_title = v
                if k == 'description':
                    meta_url.og_description = v
                if k == 'type':
                    meta_url.og_type = v
                if k == 'id':
                    meta_url.og_id = v

        meta_url.save()
        logger.info('MetaURL {} refreshed'.format(meta_url_id))
    except MetaURL.DoesNotExist:
        logger.error('MetaURL {} does not exist.'.format(meta_url_id))
