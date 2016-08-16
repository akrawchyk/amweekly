from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from amweekly.shares.models import Share, MetaURL


class ShareResource(resources.ModelResource):

    class Meta:
        model = Share


@admin.register(Share)
class ShareAdmin(ImportExportModelAdmin):
    pass


@admin.register(MetaURL)
class MetaURLAdmin(admin.ModelAdmin):
    pass
