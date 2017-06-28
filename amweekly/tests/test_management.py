from datetime import datetime

from django.core.management import call_command

import pytest


@pytest.mark.django_db
def test_postlinks_command_friday(share, mocker):
    mocked = mocker.patch('amweekly.slack.jobs.process_incoming_webhook.delay')
    mocked_dt = mocker.patch('amweekly.management.commands.postlinks.datetime.datetime')  # noqa
    mocked_dt.utcnow.return_value = datetime(2017, 6, 23)  # FRIDAY
    call_command('postlinks')
    assert mocked.called


@pytest.mark.django_db
def test_postlinks_command_not_friday(share, mocker):
    mocked = mocker.patch('amweekly.slack.jobs.process_incoming_webhook.delay')
    call_command('postlinks')
    assert not mocked.called
