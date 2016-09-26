import json
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@csrf_exempt
@require_POST
def webhook(request):
    jsondata = request.body
    data = json.loads(jsondata)

    WebhookTransaction.objects.create(
        date_event_generated=datetime.fromtimestamp(
            data['timestamp']/1000.0,
            tz=timezone.get_current_timezone()
        )
    )

    return HttpResponse(status=200)
