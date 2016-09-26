from django.db import models


class WebhookTransaction(models.Model):
    UNPROCESSED = 1
    PROCESSED = 2
    ERROR = 3

    STATUSES = (
        (UNPROCESSED, 'Unprocessed'),
        (PROCESSED, 'Processed'),
        (ERROR, 'Error'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1,
                              choices=STATUSES,
                              default=UNPROCESSED)

