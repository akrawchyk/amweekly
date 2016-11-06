from amweekly.slack.jobs import process_slash_command_webhook
from amweekly.slack.models import WebhookTransaction

import pytest

pytest.mark.integration


@pytest.mark.django_db
def test_process_slash_command_webhook(
        settings, slash_command_webhook_transaction):
    settings.SLACK_TOKENS = slash_command_webhook_transaction.body.get('token')
    process_slash_command_webhook(slash_command_webhook_transaction.id)
    slash_command_webhook_transaction.refresh_from_db()
    assert slash_command_webhook_transaction.status == \
        WebhookTransaction.PROCESSED


@pytest.mark.django_db
def test_process_slash_command_webhook_error(
        settings, slash_command_webhook_transaction):
    settings.SLACK_TOKENS = ''
    process_slash_command_webhook(slash_command_webhook_transaction.id)
    slash_command_webhook_transaction.refresh_from_db()
    assert slash_command_webhook_transaction.status == WebhookTransaction.ERROR
