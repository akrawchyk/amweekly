from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

import django_rq

from amweekly.shares.models import Share, MetaURL
from amweekly.shares.jobs import hydrate_share_meta_url, refresh_meta_url


class ShareResource(resources.ModelResource):

    class Meta:
        model = Share


def refresh_share_meta_urls(modeladmin, request, queryset):
    shares = queryset
    for share in shares:
        django_rq.enqueue(hydrate_share_meta_url, share.id)


refresh_share_meta_urls.short_description = 'Refresh OpenGraph data'


@admin.register(Share)
class ShareAdmin(ImportExportModelAdmin):
    actions = [refresh_share_meta_urls]
    date_hierarchy = 'updated_at'
    fields = ('url', 'user_name', 'title' ,)
    list_display = ('user_name', 'url', 'meta_url', 'created_at',
                    'updated_at', )
    list_filter = ('user_name', )


def refresh_meta_urls(modeladmin, request, queryset):
    meta_urls = queryset
    for meta_url in meta_urls:
        django_rq.enqueue(refresh_meta_url, meta_url.id)


refresh_meta_urls.short_description = 'Refresh OpenGraph data'


@admin.register(MetaURL)
class MetaURLAdmin(admin.ModelAdmin):
    actions = [refresh_meta_urls]
    date_hierarchy = 'updated_at'
    readonly_fields = ('og_title', 'og_description', 'og_type', 'og_id', )
    fields = ('og_title', 'og_description', 'og_type', 'og_id', )
    list_display = ('og_title', 'short_description', 'og_type', 'created_at',
                    'updated_at', )
    list_filter = ('og_type', )
