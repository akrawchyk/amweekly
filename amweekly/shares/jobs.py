from urllib.request import urlopen

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured

from amweekly.shares.models import MetaURL

import facebook


def get_facebook_access_token():
    if settings.FACEBOOK_CLIENT_ID is '' or \
       settings.FACEBOOK_CLIENT_SECRET is '':
        raise ImproperlyConfigured(
            'Facebook client id and secret not configured.')

    facebook_access_token = cache.get('facebook_access_token')
    if facebook_access_token is None:
        access_token_request = urlopen(
            'https://graph.facebook.com/oauth/access_token?client_id={}&client_secret={}&grant_type=client_credentials'.format(  #noqa
                settings.FACEBOOK_CLIENT_ID, settings.FACEBOOK_CLIENT_SECRET))
        if access_token_request.status is 200:
            text_response = access_token_request.read().decode('utf-8')
            # text_response is formatted like access_token=foo
            facebook_access_token = text_response.split('=')[1]
            cache.set('facebook_access_token', facebook_access_token, 3600)
        else:
            raise ImproperlyConfigured(
                'Facebook client id and secret are invalid.')
    return facebook_access_token


# TODO instead of doing this at post_save
#      override the save method for meta_url that updates the relationship?
#      or lookup og on share pre_save and then assign on meta_url post_save
def refresh_metaurl_for_share(share_id):
    facebook_access_token = get_facebook_access_token()
    graph = facebook.GraphAPI(facebook_access_token)
    og = graph.get_object(share.url)
    og_url = og['id']  # url as recognized by the open graph

    if og_url is not None:
        meta_url, created = MetaURL.objects.get_or_create(url=og_url)

        if 'og_object' in og:
            for k, v in og['og_object'].items():
                if k == 'title':
                    meta_url.title = v
                if k == 'description':
                    meta_url.description = v
                if k == 'type':
                    meta_url.type = v

        meta_url.save()
        # FIXME infinite loop when the job is triggered post save, which causes another save here, etc etc
        # share.meta = meta_url
        # share.save()
