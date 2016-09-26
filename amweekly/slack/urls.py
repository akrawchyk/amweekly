from django.conf.urls import url

from amweekly.slack.views import webhook


urlpatterns = [
    url(r'^incoming$', webhook, name='webhook'),
]
