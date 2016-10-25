from django.conf.urls import url

from amweekly.slack.views import slash_command_webhook


urlpatterns = [
    url(r'^slash_command_webhook$', slash_command_webhook, name='slash_commands'),
]
