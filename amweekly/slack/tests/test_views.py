from amweekly.slack.views import slash_command_webhook

import pytest

pytest.mark.integration


def test_slash_command_webhook_no_token(rf):
    request = rf.post('/slack/slash_command_webhook', data={})
    response = slash_command_webhook(request)
    assert response.status_code == 400


def test_slash_command_webhook_invalid_token(settings, rf):
    settings.SLACK_TOKENS = 'test_token'
    request = rf.post('/slack/slash_command_webhook', data={
        'token': 'bad_token'})
    response = slash_command_webhook(request)
    assert response.status_code == 400


def test_slash_command_webhook_no_command(settings, rf):
    settings.SLACK_TOKENS = 'test_token'
    request = rf.post('/slack/slash_command_webhook', data={
        'token': 'test_token'})
    response = slash_command_webhook(request)
    assert response.status_code == 400


@pytest.mark.django_db
def test_slash_command_webhook_creates_webhook_transaction(settings, rf):
    settings.SLACK_TOKENS = 'test_token'
    request = rf.post('/slack/slash_command_webhook', data={
        'token': 'test_token',
        'command': '/test_command',
        'team_id': 'team_id',
        'team_domain': 'team_domain',
        'channel_id': 'channel_id',
        'channel_name': 'channel_name',
        'user_id': 'user_id',
        'user_name': 'user_name',
        'text': 'text',
        'response_url': 'http://response/com'})
    response = slash_command_webhook(request)
    assert response.status_code == 200
