from django.contrib import admin

from amweekly.slack.models import WebhookTransaction, SlashCommand, \
    IncomingWebhook


admin.site.register(WebhookTransaction)
admin.site.register(SlashCommand)
admin.site.register(IncomingWebhook)
