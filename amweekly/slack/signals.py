import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import django_rq

from amweekly.slack.models import IncomingWebhook
from amweekly.slack.jobs import process_incoming_webhook

logger = logging.getLogger(__name__)


@receiver(post_save, sender=IncomingWebhook, dispatch_uid='handle_incoming_webhoook_schedule')  # noqa
def handle_incoming_webhook_schedule(sender, instance, **kwargs):
    scheduler = django_rq.get_scheduler('default')
    job_ids = [j.id for j in scheduler.get_jobs()]

    # check if we need to unschedule
    if instance.job_id and instance.job_id in job_ids:
        if not instance.enabled:
            scheduler.cancel(instance.job_id)
            instance.job_id = ''
            instance.save(update_fields=['job_id'])
            logger.info('Cancelled IncomingWebhook job {}'.format(
                instance.job_id))
        else:
            jobs = scheduler.get_jobs()
            for job in jobs:
                if job.id == instance.job_id:
                    if instance.crontab != job.meta['cron_string']:
                        scheduler.cancel(job.id)
                        instance.job_id = ''

    # check if we need to schedule
    if instance.enabled and not instance.job_id:
        repeat = 0
        if instance.repeat:
            repeat = None

        job = scheduler.cron(
            instance.crontab,
            func=process_incoming_webhook,
            args=[instance.id],
            repeat=repeat,
            queue_name='default')
        instance.job_id = job.id
        instance.save(update_fields=['job_id'])
        logger.info('IncomingWebhook {} is scheduled as job {}'.format(
            instance.id, instance.job_id))


@receiver(post_delete, sender=IncomingWebhook, dispatch_uid='cancel_incoming_webhook_schedule')  # noqa
def cancel_incoming_webhook_schedule(sender, instance, **kwargs):
    scheduler = django_rq.get_scheduler('default')
    job_ids = [j.id for j in scheduler.get_jobs()]

    if instance.job_id and instance.job_id in job_ids:
        scheduler.cancel(instance.job_id)
        logger.info('Cancelled IncomingWebhook job {}'.format(
            instance.job_id))
