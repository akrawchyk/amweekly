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
    shares = queryset[:5]
    for share in shares:
        django_rq.enqueue(hydrate_share_meta_url, share.id)
refresh_share_meta_urls.short_description = 'Refresh OpenGraph data (max 5)'


@admin.register(Share)
class ShareAdmin(ImportExportModelAdmin):
    actions = [refresh_share_meta_urls]


def refresh_meta_urls(modeladmin, request, queryset):
    meta_urls = queryset[:5]
    for meta_url in meta_urls:
        django_rq.enqueue(refresh_meta_url, meta_url.id)
refresh_meta_urls.short_description = 'Refresh OpenGraph data (max 5)'


@admin.register(MetaURL)
class MetaURLAdmin(admin.ModelAdmin):
    actions = [refresh_meta_urls]
