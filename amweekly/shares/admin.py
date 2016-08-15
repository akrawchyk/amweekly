from django.contrib import admin

from amweekly.shares.models import Share


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    pass
