from django.apps import AppConfig


class AmweeklyConfig(AppConfig):
    name = 'amweekly'

    def ready(self):
        import amweekly.shares.signals  # noqa

        # schedule unscheduled
