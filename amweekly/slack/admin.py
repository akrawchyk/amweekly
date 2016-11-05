from django.contrib import admin

from amweekly.slack.models import WebhookTransaction, SlashCommand, \
    IncomingWebhook


@admin.register(WebhookTransaction)
class WebhookTransactionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    fields = ('content_type', 'status', 'body', 'headers')
    list_display = ('content_type', 'created_at', 'status')
    list_filter = ('status', )


@admin.register(SlashCommand)
class SlashCommandAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('user_name', 'team_domain', 'channel_name', 'command',
                    'created_at')
    list_filter = ('user_name', 'team_domain', 'channel_name', 'command', )


admin.site.register(IncomingWebhook)
