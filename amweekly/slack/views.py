import json
import logging

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from amweekly.slack.models import WebhookTransaction
from amweekly.slack.jobs import process_slash_command_webhook

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def slash_command_webhook(request):
    body_json = json.dumps(request.POST.dict())

    print(request.META)

    webhook_transaction = WebhookTransaction.objects.create(
        body=body_json,
        request_meta={'0': 1}  # FIXME
    )

    token = request.POST.get('token')

    if not token:
        logger.error(
            'WebhookTransaction with id {} does not have a token.'.format(
                webhook_transaction.id))
        return HttpResponse(status=400)

    if token not in settings.SLACK_TOKENS:
        logger.error(
            'WebhookTransaction with id {} has unrecognized token.'.format(
                webhook_transaction.id))
        return HttpResponse(status=400)

    command = request.POST.get('command')

    if not command:
        logger.error(
            'WebhookTransaction with id {} is not a Slash Command.'.format(
                webhook_transaction.id))
        print('no command')
        return HttpResponse(status=400)

    process_slash_command_webhook(webhook_transaction.id)
    return HttpResponse(status=200)
