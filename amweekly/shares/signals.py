from django.db.models.signals import post_save
from django.dispatch import receiver

import django_rq

from amweekly.shares.models import Share
from amweekly.shares.jobs import fetch_opengraph_data_for_share


@receiver(post_save, sender=Share, dispatch_uid='get_share_meta_url')
def get_share_meta_url(sender, share, **kwargs):
    django_rq.enqueue(fetch_opengraph_data_for_share, share)
