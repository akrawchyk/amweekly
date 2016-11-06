from datetime import datetime, timedelta

from django.db.models.signals import post_save

from amweekly.slack.models import WebhookTransaction

from factory import Faker, lazy_attribute, lazy_attribute_sequence
from factory.django import DjangoModelFactory, mute_signals


class WebhookTransactionFactory(DjangoModelFactory):
    class Meta:
        model = 'slack.WebhookTransaction'

    status = WebhookTransaction.UNPROCESSED
    body = {}
    headers = {}


class SlashCommandWebhookTransactionFactory(DjangoModelFactory):
    class Meta:
        model = 'slack.WebhookTransaction'

    status = WebhookTransaction.UNPROCESSED
    headers = {}

    @lazy_attribute_sequence
    def body(self, n):
        return {
            "text": "http://test-url{}.com".format(n),
            "channel_id": "test_channel_id{}".format(n),
            "response_url": "https://hooks.slack.com/commands/test/url{}".format(n),  # noqa
            "user_name": "andrew{}".format(n),
            "channel_name": "directmessage",
            "team_domain": "test_domain{}".format(n),
            "token": "test_token{}".format(n),
            "team_id": "test_team_id{}".format(n),
            "command": "/test_command{}".format(n),
            "user_id": "test_user_id{}".format(n)}


@mute_signals(post_save)
class SlashCommandFactory(DjangoModelFactory):
    class Meta:
        model = 'slack.SlashCommand'

    token = Faker('md5', raw_output=False)
    team_id = Faker('md5', raw_output=False)
    team_domain = Faker('word')
    channel_id = Faker('md5', raw_output=False)
    channel_name = Faker('word')
    user_id = Faker('md5', raw_output=False)
    user_name = Faker('profile', fields='username')
    command = '{}{}'.format('/', Faker('word'))
    text = Faker('sentence')
    response_url = Faker('url')


class IncomingWebhookFactory(DjangoModelFactory):
    class Meta:
        model = 'slack.IncomingWebhook'

    enabled = False
    repeat = False
    job_id = ''
    webhook_url = Faker('url')
    text = Faker('sentence')
    username = Faker('profile', fields='username')
    icon_emoji = ':ghost:'
    icon_url = ''

    @lazy_attribute
    def crontab(self):
        now = datetime.now()
        future_time = now + timedelta(minutes=10)
        return '{} * * * *'.format(future_time.minute)
