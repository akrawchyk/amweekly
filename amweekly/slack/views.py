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
        logger.error('Slash Command request does not have a token.')
        return HttpResponse(status=400)

    if token not in settings.SLACK_TOKENS:
        logger.error('Slash Command request has an unrecognized token.')
        return HttpResponse(status=400)

    command = request.POST.get('command')

    if not command:
        logger.error('Slash Command request is not a Slash Command.')
        return HttpResponse(status=400)

    webhook_transaction = WebhookTransaction.objects.create(
        body=request.POST.dict(),
        request_meta={}  # TODO: copy request.META here
    )

    message = process_slash_command_webhook(webhook_transaction.id)
    return HttpResponse(message, status=200)
