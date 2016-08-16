from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

import django_rq

from amweekly.shares.models import Share, MetaURL
from amweekly.shares.jobs import refresh_metaurl_for_share


class ShareResource(resources.ModelResource):

    class Meta:
        model = Share


def refresh_share_meta(modeladmin, request, queryset):
    shares = queryset[:5]
    for share in shares:
        django_rq.enqueue(refresh_metaurl_for_share, share)
refresh_share_meta.short_description = 'Refresh OpenGraph data for share (max 5)'  # noqa


@admin.register(Share)
class ShareAdmin(ImportExportModelAdmin):
    actions = [refresh_share_meta]


@admin.register(MetaURL)
class MetaURLAdmin(admin.ModelAdmin):
    pass
