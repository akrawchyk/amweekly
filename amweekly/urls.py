from django.conf.urls import include, url
from django.contrib import admin

from amweekly.views import HomePageView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),

    url(r'^slack/', include('amweekly.slack.urls')),

    url(r'^admin/rq/', include('django_rq.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
