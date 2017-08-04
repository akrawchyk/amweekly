from __future__ import unicode_literals

from django.views.generic import TemplateView

from amweekly.shares.models import Share


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        shares = Share.objects.all().order_by('-created_at')[:10]
        context['shares'] = shares
        return context
