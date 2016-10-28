from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from crontab import CronTab


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
    status = models.CharField(max_length=1,
                              choices=STATUSES,
                              default=UNPROCESSED)

    class Meta:
        abstract = True


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


class IncomingWebhook(models.Model):
    """
    Incoming Webhooks are a simple way to post messages from external sources
    into Slack. They make use of normal HTTP requests with a JSON payload that
    includes the message text and some options.

    N.B. - Message attachments are not supported

    See docs at https://api.slack.com/incoming-webhooks.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    crontab = models.CharField(max_length=255)
    webhook_transactions = GenericRelation(WebhookTransaction)

    webhook_url = models.URLField()
    text = models.TextField(blank=True)
    username = models.CharField(max_length=255, blank=True)
    icon_emoji = models.CharField(max_length=255, blank=True)
    icon_url = models.URLField(blank=True)

    def clean(self):
        try:
            CronTab(self.crontab)
        except:
            raise ValidationError(_('Unrecognized crontab `{}`').format(
                self.crontab))


# TODO make a scheduled class for recovering after shutdown for repeatable
