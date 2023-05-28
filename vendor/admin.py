from django.contrib import admin
from .models import Vendor, OpeningHour


class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vender_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'vender_name')
    list_editable = ('is_approved',)


class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'day', 'from_hour', 'to_hour')

admin.site.register(Vendor, VendorAdmin)
admin.site.register(OpeningHour)