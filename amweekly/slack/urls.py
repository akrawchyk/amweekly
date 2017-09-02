from django.conf.urls import url

from amweekly.slack.views import slash_command_webhook, events_challenge_response


urlpatterns = [
    url(r'^slash_command_webhook/$', slash_command_webhook, name='slash_commands'),  # noqa

    url(r'^events\/challenge_response$', events_challenge_response)
]
