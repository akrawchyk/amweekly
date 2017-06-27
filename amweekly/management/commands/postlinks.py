import datetime
import logging

from django.core.management.base import BaseCommand

from amweekly.slack.jobs import process_incoming_webhook

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

logger = logging.getLogger('amweekly.command')


class Command(BaseCommand):
    help = 'Post links from the past week to Slack'

    def handle(self, *args, **options):

        today = datetime.datetime.utcnow().date()

        if today.weekday() == FRIDAY:
            logger.info('Skip posting to Slack, we only post on Friday')
            return

        end = datetime.datetime.combine(
            today, datetime.time(11, 59, 59))
        start = datetime.datetime.combine(
            today - datetime.timedelta(days=7), datetime.time(12, 0, 0))

        logger.info(f'Collecting shares from {start} to {end}')

        process_incoming_webhook.delay(start, end)
