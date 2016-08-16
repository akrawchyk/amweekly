from django.db.models.signals import post_save
from django.dispatch import receiver

import django_rq

from amweekly.shares.models import Share
from amweekly.shares.jobs import refresh_metaurl_for_share


@receiver(post_save, sender=Share, dispatch_uid='refresh_share_meta_url')
def refresh_share_meta_url(sender, instance, **kwargs):
    django_rq.enqueue(refresh_metaurl_for_share, instance)
