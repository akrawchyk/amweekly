import datetime
import logging
import random

from django.conf import settings
from django.core.management.base import BaseCommand

from amweekly.shares.models import Share

logger = logging.getLogger('amweekly.command')


class Command(BaseCommand):
    help = 'Post links from the past week to Slack'

    def handle(self, *args, **options):

        if not settings.DEBUG:
            logger.warn('Sorry, can only scramble data in DEBUG')

        today = datetime.datetime.utcnow().date()

        for share in Share.objects.all():
            share.created_at = \
                today - datetime.timedelta(days=random.randint(1, 6))
            share.save()
