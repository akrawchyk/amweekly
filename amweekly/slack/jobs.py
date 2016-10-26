import logging

from amweekly.slack.models import WebhookTransaction, SlashCommand
from amweekly.shares.models import Share

logger = logging.getLogger(__name__)


def process_slash_command_webhook(webhook_transaction_id):
    webhook_transaction = WebhookTransaction.objects.get(
        pk=webhook_transaction_id)

    try:
        slash_command = SlashCommand.objects.create(
            token=webhook_transaction.body.get('token'),
            team_id=webhook_transaction.body.get('team_id'),
            team_domain=webhook_transaction.body.get('team_domain'),
            channel_id=webhook_transaction.body.get('channel_id'),
            channel_name=webhook_transaction.body.get('channel_name'),
            user_id=webhook_transaction.body.get('user_id'),
            user_name=webhook_transaction.body.get('user_name'),
            command=webhook_transaction.body.get('command'),
            text=webhook_transaction.body.get('text'),
            response_url=webhook_transaction.body.get('response_url'),
            webhook_transaction=webhook_transaction
        )

        Share.objects.create(
            user_name=slash_command.user_name,
            url=slash_command.text
        )

        webhook_transaction.status = WebhookTransaction.PROCESSED
        webhook_transaction.save()
        return 'Slack Command {} processed successfully'.format(
                slash_command.command)
    except Exception as e:
        logger.error(
            'WebhookTransaction with id {} failed to process: {}'.format(
                webhook_transaction_id, str(e)))
        webhook_transaction.status = WebhookTransaction.ERROR
        webhook_transaction.save()
        return 'Failed to process Slash Command {}'.format(
            slash_command.command)
