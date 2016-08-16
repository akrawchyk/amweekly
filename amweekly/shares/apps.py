from django.apps import AppConfig


class SharesConfig(AppConfig):
    name = 'shares'

    def ready(self):
        import amweekly.shares.signals  # noqa
