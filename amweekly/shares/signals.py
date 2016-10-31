from django.db.models.signals import post_save
from django.dispatch import receiver

import django_rq

from amweekly.shares.models import Share
from amweekly.shares.jobs import hydrate_share_meta_url


@receiver(post_save, sender=Share, dispatch_uid='hydrate_meta_url_for_share')
def hydrate_meta_url_for_share(sender, instance, **kwargs):
    django_rq.enqueue(hydrate_share_meta_url, instance.id)
