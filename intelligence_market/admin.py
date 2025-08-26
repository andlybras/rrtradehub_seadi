from django.contrib import admin
from .models import AnalysisPage, Chart
from .forms import ChartAdminForm  # <-- 1. Importe o novo formulário

@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    form = ChartAdminForm  # <-- 2. Diga ao admin para usar nosso formulário
    list_display = ('name', 'slug', 'shortcode_display')
    readonly_fields = ('slug',)
    search_fields = ('name',)

    def shortcode_display(self, obj):
        return obj.get_shortcode()
    shortcode_display.short_description = "Shortcode (para copiar)"
    
    # 3. Ocultamos o campo JSON original, pois nosso formulário já cuida dele.
    exclude = ('options_json',)


@admin.register(AnalysisPage)
class AnalysisPageAdmin(admin.ModelAdmin):
    list_display = ('card_title', 'is_published', 'updated_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'card_title')