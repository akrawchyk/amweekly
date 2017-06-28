import json
import logging

import requests
from django_rq import job

from amweekly.shares.models import Share
from amweekly.slack.models import IncomingWebhook, SlashCommand, \
    WebhookTransaction


logger = logging.getLogger('amweekly.jobs')


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
            webhook_transaction=webhook_transaction)

        webhook_transaction.status = WebhookTransaction.PROCESSED
        webhook_transaction.integration = slash_command
        webhook_transaction.save()
        logger.info('SlashCommand {} processed successfully'.format(
            slash_command.id))
        return 'Saved the url {}, thanks for sharing!'.format(
            webhook_transaction.body.get('text'))
    except Exception as e:
        webhook_transaction.status = WebhookTransaction.ERROR
        webhook_transaction.save()
        log = 'WebhookTransaction {} failed to process as SlashCommand: {}'.format(  # noqa
            webhook_transaction.id, str(e))
        return log


@job
def process_incoming_webhook(start, end):
    for incoming_webhook in IncomingWebhook.objects.filter(enabled=True):

        shares = Share.objects.between_dates(start, end)

        attachment = {
            'fallback': f'Antimatter Weekly URLs for {start.date()} through {end.date()}',  # noqa
            # 'pretext': '',
            # 'text': '',
            'fields': [],
        }

        for share in shares:
            share_doc = {
                'title': f'shared by {share.user_name}',
                'value': share.slack_format(),
                'short': False,
            }
            attachment['fields'].append(share_doc)

        message = {
            'text': f'Antimatter Weekly URLs for {start.date()} through {end.date()}',  # noqa
            'attachments': [attachment]
        }
        kwargs = {'headers': {'Content-type': 'application/json'}}

        if incoming_webhook.username:
            message['username'] = incoming_webhook.username

        if incoming_webhook.icon_emoji:
            message['icon_emoji'] = incoming_webhook.icon_emoji

        kwargs['data'] = json.dumps(message)

        webhook_transaction = WebhookTransaction.objects.create(
            body=message,
            headers=kwargs['headers'],
            integration=incoming_webhook)

        try:
            r = requests.post(
                incoming_webhook.webhook_url,
                **kwargs)
            logger.info(f'{r.status_code}: {r.content}')
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
                    incoming_webhook.pk, str(e)))
