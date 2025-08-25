from django.contrib import admin
from .models import SiteAsset

@admin.register(SiteAsset)
class SiteAssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'asset_type', 'order')
    list_filter = ('asset_type',)
    search_fields = ('name',)
    list_editable = ('order',)
