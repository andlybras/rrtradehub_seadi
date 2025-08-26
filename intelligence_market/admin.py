from django.contrib import admin
from .models import AnalysisPage, Chart

@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'shortcode_display')
    readonly_fields = ('slug',)
    search_fields = ('name',)

    def shortcode_display(self, obj):
        return obj.get_shortcode()
    shortcode_display.short_description = "Shortcode (para copiar)"

@admin.register(AnalysisPage)
class AnalysisPageAdmin(admin.ModelAdmin):
    list_display = ('card_title', 'is_published', 'updated_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'card_title')