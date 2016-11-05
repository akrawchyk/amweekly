from amweekly.slack.models import WebhookTransaction

from django.db.models.signals import post_save

from factory import Faker
from factory.django import DjangoModelFactory, mute_signals


class WebhookTransactionFactory(DjangoModelFactory):
    class Meta:
        model = 'slack.WebhookTransaction'

    status = WebhookTransaction.UNPROCESSED
    body = {}
    headers = {}


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

    webhook_url = Faker('url')
    text = Faker('sentence')
    username = Faker('profile', fields='username')
    icon_emoji = ':ghost:'
    icon_url = None
