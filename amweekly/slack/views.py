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
    token = request.POST.get('token')

    if not token:
        logger.error('Webhook request does not have a token.')
        return HttpResponse(status=400)

    if token not in settings.SLACK_TOKENS:
        logger.error('Webhook request has an unrecognized token.')
        return HttpResponse(status=400)

    command = request.POST.get('command')

    if not command:
        logger.error('Webhook request is not a command.')
        return HttpResponse(status=400)

    webhook_transaction = WebhookTransaction.objects.create(
        body=request.POST.dict(),
        headers={})  # TODO: copy request.META here

    logger.info('Processing WebhookTransaction {}'.format(
        webhook_transaction.id))
    message = process_slash_command_webhook(webhook_transaction.id)
    return HttpResponse(message, status=200)
