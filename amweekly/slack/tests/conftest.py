from amweekly.slack.tests.factories import SlashCommandFactory, \
    IncomingWebhookFactory, WebhookTransactionFactory, \
    SlashCommandWebhookTransactionFactory

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


@pytest.fixture
def slash_command_webhook_transaction():
    return SlashCommandWebhookTransactionFactory()
