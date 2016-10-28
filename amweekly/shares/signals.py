from django.db.models.signals import post_save
from django.dispatch import receiver

import django_rq

from amweekly.shares.models import Share, MetaURL
from amweekly.shares.jobs import refresh_meta_url


@receiver(post_save, sender=Share, dispatch_uid='refresh_meta_url_for_share')
def refresh_meta_url_for_share(sender, instance, **kwargs):
    meta_url, created = MetaURL.objects.get_or_create(og_url=instance.url)
    if created:
        meta_url.share_set.add(instance)
    django_rq.enqueue(refresh_meta_url, meta_url.id)
