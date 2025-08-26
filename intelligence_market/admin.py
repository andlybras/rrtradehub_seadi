from django.contrib import admin
from .models import AnalysisPage, Chart

@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    # Voltamos a definir os campos que queremos ver diretamente aqui
    fields = ('name', 'options_json')
    list_display = ('name', 'slug', 'shortcode_display')
    readonly_fields = ('slug',) # O slug continua sendo gerado automaticamente
    search_fields = ('name',)

    def shortcode_display(self, obj):
        return obj.get_shortcode()
    shortcode_display.short_description = "Shortcode (para copiar)"

@admin.register(AnalysisPage)
class AnalysisPageAdmin(admin.ModelAdmin):
    list_display = ('card_title', 'is_published', 'updated_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'card_title')