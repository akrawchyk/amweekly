from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from amweekly.shares.models import Share


class ShareResource(resources.ModelResource):

    class Meta:
        model = Share


@admin.register(Share)
class ShareAdmin(ImportExportModelAdmin):
    pass
