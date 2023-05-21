from django.contrib import admin
from .models import Vendor


class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vender_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'vender_name')

admin.site.register(Vendor, VendorAdmin)
