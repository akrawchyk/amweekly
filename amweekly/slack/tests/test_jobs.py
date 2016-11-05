from amweekly.slack.jobs import process_slash_command_webhook
from amweekly.slack.models import WebhookTransaction

import pytest

pytest.mark.integration


@pytest.mark.django_db
def test_process_slash_command_webhook(settings, webhook_transaction):
    settings.SLACK_TOKENS = 'test_token'
    webhook_transaction.body = {
        "text": "http://reddit.com",
        "channel_id": "test_channel_id",
        "response_url": "https://hooks.slack.com/commands/test/url",
        "user_name": "andrew",
        "channel_name": "directmessage",
        "team_domain": "isl",
        "token": "test_token",
        "team_id": "test_team_id",
        "command": "/amweekly",
        "user_id": "test_user_id"}
    webhook_transaction.save()
    process_slash_command_webhook(webhook_transaction.id)
    webhook_transaction.refresh_from_db()
    assert webhook_transaction.status == WebhookTransaction.PROCESSED


@pytest.mark.django_db
def test_process_slash_command_webhook_error(webhook_transaction):
    process_slash_command_webhook(webhook_transaction.id)
    webhook_transaction.refresh_from_db()
    assert webhook_transaction.status == WebhookTransaction.ERROR
