import json
import logging

from amweekly.slack.models import WebhookTransaction, SlashCommand

logger = logging.getLogger(__name__)


def process_slash_command_webhook(webhook_transaction_id):
    webhook_transaction = WebhookTransaction.objects.get(
        pk=webhook_transaction_id)

    try:
        body_json = json.loads(webhook_transaction.body)

        SlashCommand.objects.create(
            token=body_json.get('token'),
            team_id=body_json.get('team_id'),
            team_domain=body_json.get('team_domain'),
            channel_id=body_json.get('channel_id'),
            channel_name=body_json.get('channel_name'),
            user_id=body_json.get('user_id'),
            user_name=body_json.get('user_name'),
            command=body_json.get('command'),
            text=body_json.get('text'),
            response_url=body_json.get('response_url'),
            webhook_transaction=webhook_transaction
        )

        # TODO use the command to provide a response

        webhook_transaction.status = WebhookTransaction.PROCESSED
        webhook_transaction.save()
    except Exception as e:
        logger.error(
            'WebhookTransaction with id {} failed to process: {}'.format(
                webhook_transaction_id, str(e)))
        webhook_transaction.status = WebhookTransaction.ERROR
        webhook_transaction.save()
