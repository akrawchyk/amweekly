from django.contrib import admin

from amweekly.slack.models import WebhookTransaction, SlashCommand, \
    IncomingWebhook


@admin.register(WebhookTransaction)
class WebhookTransactionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    fields = ('content_type', 'status', 'body', 'headers')
    list_display = ('content_type', 'created_at')


@admin.register(SlashCommand)
class SlashCommandAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('user_name', 'team_domain', 'command', 'created_at')


admin.site.register(IncomingWebhook)
