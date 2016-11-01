from datetime import datetime, timedelta
import logging

from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

import django_rq

from amweekly.slack.jobs import process_incoming_webhook

from crontab import CronTab

logger = logging.getLogger(__name__)


class BaseTransaction(models.Model):
    """
    Used to track the status of a transaction.
    """
    UNPROCESSED = 1
    PROCESSED = 2
    ERROR = 3
    STATUSES = (
        (UNPROCESSED, 'Unprocessed'),
        (PROCESSED, 'Processed'),
        (ERROR, 'Error'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(
        choices=STATUSES,
        default=UNPROCESSED)

    class Meta:
        abstract = True


class BaseSchedulable(models.Model):
    """
    Used to schedule Slack jobs with a crontab
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)
    job_id = models.CharField(blank=True, max_length=255)
    crontab = models.CharField(max_length=255)
    repeat = models.BooleanField(default=False)

    def clean(self):
        try:
            CronTab(self.crontab)
        except:
            raise ValidationError(_('Unrecognized crontab `{}`').format(
                self.crontab))


class WebhookTransaction(BaseTransaction, models.Model):
    """
    Represents a webhook transaction with Slack. Stores raw transaction data as
    JSON.
    """
    body = JSONField()
    headers = JSONField()
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    integration = GenericForeignKey()

    def __str__(self):
        return u'{0}'.format(self.created_at)


class SlashCommand(models.Model):
    """
    Slash Commands enable Slack users to interact with external services
    directly from Slack.

    See docs at https://api.slack.com/slash-commands.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    webhook_transaction = models.OneToOneField(WebhookTransaction)

    token = models.CharField(max_length=255)
    team_id = models.CharField(max_length=255)
    team_domain = models.CharField(max_length=255)
    channel_id = models.CharField(max_length=255)
    channel_name = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    command = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    response_url = models.URLField()


class IncomingWebhook(BaseSchedulable, models.Model):
    """
    Incoming Webhooks are a simple way to post messages from external sources
    into Slack. They make use of normal HTTP requests with a JSON payload that
    includes the message text and some options.

    N.B. - Message attachments are not supported

    See docs at https://api.slack.com/incoming-webhooks.
    """
    webhook_transactions = GenericRelation(WebhookTransaction)
    webhook_url = models.URLField()
    text = models.TextField(blank=True)
    username = models.CharField(max_length=255, blank=True)
    icon_emoji = models.CharField(max_length=255, blank=True)
    icon_url = models.URLField(blank=True)
    scheduled_for = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        scheduler = django_rq.get_scheduler('default')
        job_ids = [j.id for j in scheduler.get_jobs()]

        # check if we need to unschedule
        if self.job_id and self.job_id in job_ids:
            if not self.enabled:
                scheduler.cancel(self.job_id)
                self.job_id = ''
                self.scheduled_for = None
                logger.info('Deleted job {}'.format(self.job_id))

        # check if we need to schedule
        if self.enabled and not self.job_id:
            schedule_for = self.get_next_scheduled()
            job = scheduler.enqueue_at(
                schedule_for,
                process_incoming_webhook,
                self.id)
            self.job_id = job.id
            self.scheduled_for = schedule_for
            logger.info('IncomingWebhook {} is scheduled for {}'.format(
                self.id, schedule_for))

        super(IncomingWebhook, self).save(*args, **kwargs)

    @property
    def scheduled(self):
        return self.job_id is not ''

    def get_next_scheduled(self):
        next = CronTab(self.crontab).next()
        return datetime.now() + timedelta(seconds=next)

# TODO make a scheduled class for recovering after shutdown for repeatable
