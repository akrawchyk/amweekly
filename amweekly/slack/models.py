import logging

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models


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

    def is_scheduled(self):
        return self.job_id is not ''
    is_scheduled.boolean = True


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
        super(IncomingWebhook, self).save(*args, **kwargs)
