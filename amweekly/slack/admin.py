from django.contrib import admin

from amweekly.slack.models import WebhookTransaction, SlashCommand, \
    IncomingWebhook


@admin.register(WebhookTransaction)
class WebhookTransactionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    fields = ('content_type', 'status', 'body', 'headers', )
    list_display = ('content_type', 'status', 'created_at', )
    list_filter = ('status', )


@admin.register(SlashCommand)
class SlashCommandAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    readonly_fields = ('command', 'text', 'token', 'team_id', 'team_domain',
                       'channel_id', 'channel_name', 'user_id', 'user_name',
                       'response_url', 'webhook_transaction')
    list_display = ('user_name', 'team_domain', 'channel_name', 'command',
                    'created_at', )
    list_filter = ('user_name', 'team_domain', 'channel_name', 'command', )


@admin.register(IncomingWebhook)
class IncomingWebhookAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    readonly_fields = ('job_id', )
    list_display = ('username', 'enabled', 'is_scheduled',)
    list_filter = ('username', 'enabled', )
