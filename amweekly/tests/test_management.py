from django.core.management import call_command
from freezegun import freeze_time

import pytest


@pytest.mark.django_db
def test_postlinks_command_friday(share, mocker):
    mocked = mocker.patch('amweekly.slack.jobs.process_incoming_webhook.delay')
    with freeze_time("2017-06-23"):
        call_command('postlinks')
    assert mocked.called


@pytest.mark.django_db
def test_postlinks_command_not_friday(share, mocker):
    mocked = mocker.patch('amweekly.slack.jobs.process_incoming_webhook.delay')
    with freeze_time("2017-06-22"):
        call_command('postlinks')
    assert not mocked.called
