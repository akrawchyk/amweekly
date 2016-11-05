from django.apps import AppConfig


class AmweeklyConfig(AppConfig):
    name = 'amweekly'

    def ready(self):
        import amweekly.shares.signals  # noqa
        import amweekly.signals  # noqa

        # IncomingWebhook = self.get_model('IncomingWebhook')

        # find enabled jobs that have no job id
        # scheduled them
