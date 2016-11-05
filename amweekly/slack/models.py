import logging

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

import django_rq

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

    class Meta:
        abstract = True

    # TODO crontab validator? thanks solomon
    def clean(self, *args, **kwargs):
        try:
            CronTab(self.crontab)
        except:
            raise ValidationError(_('Unrecognized crontab `{}`').format(
                self.crontab))
        super(BaseSchedulable, self).clean(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        # ensure token is recognized
        if self.token not in settings.SLACK_TOKENS:
            raise ValidationError('Unrecognized Slack token')

        super(SlashCommand, self).save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        self.full_clean()

        scheduler = django_rq.get_scheduler('default')
        job_ids = [j.id for j in scheduler.get_jobs()]

        # check if we need to unschedule
        if self.job_id and self.job_id in job_ids:
            if not self.enabled:
                self.unschedule(scheduler)

        # check if we need to schedule
        if self.enabled and not self.job_id:
            self.schedule(scheduler)

        super(IncomingWebhook, self).save(*args, **kwargs)

    @property
    def scheduled(self):
        return self.job_id is not ''

    def schedule(self, scheduler):
        from amweekly.slack.jobs import process_incoming_webhook
        repeat = 0
        if self.repeat:
            repeat = None

        job = scheduler.cron(
            self.crontab,
            func=process_incoming_webhook,
            args=[self.id],
            repeat=repeat,
            queue_name='default')
        self.job_id = job.id
        logger.info(_('IncomingWebhook {} is scheduled for {}').format(
            self.id))

    def unschedule(self, scheduler):
        scheduler.cancel(self.job_id)
        self.job_id = ''
        logger.info(_('Cancelled IncomingWebhook job {}').format(self.job_id))


# TODO make a scheduled class for recovering after shutdown for repeatable
