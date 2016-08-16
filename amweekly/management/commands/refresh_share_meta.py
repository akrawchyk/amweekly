from django.core.management.base import BaseCommand, CommandError

import django_rq

from amweekly.shares.models import Share
from amweekly.shares.jobs import fetch_opengraph_data_for_share


class Command(BaseCommand):
    help = 'Fetches fresh open graph data for specified shares'

    def add_arguments(self, parser):
        parser.add_argument('share_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for share_id in options['share_id']:
            try:
                share = Share.objects.get(pk=share_id)
                django_rq.enqueue(fetch_opengraph_data_for_share, share)
            except Share.DoesNotExist:
                raise CommandError('Share {} doesn\'t exist.'.format(share_id))
