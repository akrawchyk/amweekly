import django_rq

from amweekly.slack.tests.factories import SlashCommandFactory, \
    IncomingWebhookFactory, WebhookTransactionFactory, \
    SlashCommandWebhookTransactionFactory

import pytest


@pytest.fixture
def scheduler():
    scheduler = django_rq.get_scheduler('default')
    prev_jobs = scheduler.get_jobs()
    yield scheduler
    # remove scheduled test jobs
    jobs = scheduler.get_jobs()
    for j in jobs:
        found = False
        for pj in prev_jobs:
            if pj.id == j.id:
                found = True
        if not found:
            scheduler.cancel(j.id)


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
