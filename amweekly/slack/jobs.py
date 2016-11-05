import json
import logging

# from django.apps import AppConfig

from amweekly.slack.models import IncomingWebhook, SlashCommand, WebhookTransaction

import requests

logger = logging.getLogger(__name__)


def process_slash_command_webhook(webhook_transaction_id):
    # WebhookTransaction = AppConfig.get_model('slack.WebhookTransaction')
    webhook_transaction = WebhookTransaction.objects.get(
        pk=webhook_transaction_id)

    try:
        # SlashCommand = AppConfig.get_model('slack.SlashCommand')
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
            webhook_transaction=webhook_transaction)

        webhook_transaction.status = WebhookTransaction.PROCESSED
        webhook_transaction.integration = slash_command
        webhook_transaction.save()
        log = 'SlashCommand {} processed successfully'.format(
            slash_command.id)
        logger.info(log)
        return log
    except Exception as e:
        webhook_transaction.status = WebhookTransaction.ERROR
        webhook_transaction.save()
        log = 'SlashCommand {} failed to process: {}'.format(
            slash_command.id, str(e))
        return log


def process_incoming_webhook(incoming_webhook_id):
    try:
        # IncomingWebhook = AppConfig.get_model('slack.IncomingWebhook')
        incoming_webhook = IncomingWebhook.objects.get(pk=incoming_webhook_id)
        headers = {
            'Content-type': 'application/json', }
        message = {
            'text': incoming_webhook.text, }
        kwargs = {
            'headers': headers, }

        if incoming_webhook.username:
            message['username'] = incoming_webhook.username

        if incoming_webhook.icon_emoji:
            message['icon_emoji'] = incoming_webhook.icon_emoji

        kwargs['data'] = json.dumps(message)

        # WebhookTransaction = AppConfig.get_model('slack.WebhookTransaction')
        webhook_transaction = WebhookTransaction.objects.create(
            body=message,
            headers=kwargs['headers'],
            integration=incoming_webhook)

        try:
            r = requests.post(
                incoming_webhook.webhook_url,
                **kwargs)
            r.raise_for_status()
            webhook_transaction.status = WebhookTransaction.PROCESSED
            webhook_transaction.save()
            logger.info('IncomingWebhook {} processed successfully'.format(
                incoming_webhook.id))
        except Exception as e:
            webhook_transaction.status = WebhookTransaction.ERROR
            webhook_transaction.save()
            logger.error(
                'IncomingWebhook {} failed to POST: {}'.format(
                    incoming_webhook_id, str(e)))
    except IncomingWebhook.DoesNotExist:
        logger.error(
            'IncomingWebhook with id {} does not exist'.format(
                incoming_webhook_id))
