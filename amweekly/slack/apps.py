import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class SlackConfig(AppConfig):
    name = 'slack'
