from django.db import models
from django.contrib.postgres.fields import JSONField


class WebhookTransaction(models.Model):
    """
    Used to track the status of transactions with Slack. Stores raw request
    data as JSON.
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
    body = JSONField()
    request_meta = JSONField()

    def __unicode__(self):
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

    webhook_url = models.URLField()
    text = models.TextField(blank=True)
    username = models.CharField(max_length=255, blank=True)
    icon_emoji = models.CharField(max_length=255, blank=True)
