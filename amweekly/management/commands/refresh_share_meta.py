from django.core.management.base import BaseCommand, CommandError

import django_rq

from amweekly.shares.models import Share
from amweekly.shares.jobs import refresh_share_meta_url


class Command(BaseCommand):
    help = 'Fetches fresh open graph data for specified shares'

    def add_arguments(self, parser):
        parser.add_argument('share_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for share_id in options['share_id']:
            try:
                django_rq.enqueue(refresh_share_meta_url, share_id)
            except Share.DoesNotExist:
                raise CommandError('Share {} does not exist.'.format(share_id))
