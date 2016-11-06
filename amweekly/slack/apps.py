import logging

from django.apps import AppConfig

import django_rq

logger = logging.getLogger(__name__)


class SlackConfig(AppConfig):
    name = 'slack'

    # TODO https://docs.djangoproject.com/en/1.10/ref/applications/#django.apps.AppConfig.ready
    # def ready(self):
    #     logger.info('slack ready')
    #     IncomingWebhook = self.get_model('IncomingWebhook')
    #
    #     # find scheduled incoming webhooks and ensure they are in the queue
    #     iws = IncomingWebhook.objects.filter(enabled=True)
    #     scheduler = django_rq.get_scheduler('default')
    #     job_ids = [j.id for j in scheduler.get_jobs()]
    #     for iw in iws:
    #         if not iw.job_id or iw.job_id not in job_ids:
    #             # need to schedule
    #             iw.job_id = ''
    #             iw.save()
    #             logger.info('IncomingWebhook {} rescheduled as {}'.format(
    #                 iw.id, iw.job_id))
