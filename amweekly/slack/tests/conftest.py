from amweekly.slack.tests.factories import SlashCommandFactory, \
    IncomingWebhookFactory, WebhookTransactionFactory

import pytest


@pytest.fixture
def slash_command():
    return SlashCommandFactory()


@pytest.fixture
def incoming_webhook():
    return IncomingWebhookFactory()


@pytest.fixture
def webhook_transaction():
    return WebhookTransactionFactory()
