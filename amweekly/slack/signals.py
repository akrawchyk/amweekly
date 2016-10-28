from datetime import timedelta
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from crontab import CronTab
import django_rq

from amweekly.slack.models import IncomingWebhook
from amweekly.slack.jobs import process_incoming_webhook

logger = logging.getLogger(__name__)


@receiver(post_save, sender=IncomingWebhook, dispatch_uid='schedule_incoming_webhook')  # noqa
def schedule_incoming_webhook(sender, instance, **kwargs):
    logger.info('IncomingWebhook {} processed'.format(instance.id))
    process_incoming_webhook(instance.id)
    # TODO
    # refactor this logic to:
    #  * dedupe previously scheduled crons
    #  * support repeating incoming webhooks
    #  * support rescheduling after shutdown
    # next = CronTab(instance.crontab).next()
    # scheduler = django_rq.get_scheduler('default')
    # scheduler.enqueue_in(
    #     timedelta(seconds=next),
    #     process_incoming_webhook,
    #     instance.id)
