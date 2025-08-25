from django.contrib import admin
from .models import CNAE, Company

@admin.register(CNAE)
class CNAEAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'owner', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('nome_fantasia', 'razao_social', 'cnpj', 'owner__username')
    list_editable = ('status',)
    fieldsets = (
        ('Dados do Proprietário', {'fields': ('owner',)}),
        ('Dados Empresariais', {
            'fields': (
                'razao_social', 'nome_fantasia', 'cnpj', 'inscricao_estadual',
                'main_activity', 'secondary_activities', 'logo'
            )
        }),
        ('Informações de Contato', {
            'fields': ('institutional_contact', 'institutional_email', 'address')
        }),
        ('Dados do Responsável Legal', {
            'fields': ('legal_rep_name', 'legal_rep_role', 'legal_rep_contact', 'legal_rep_email')
        }),
        ('Moderação', {
            'fields': ('status', 'moderation_notes')
        }),
    )
    
    filter_horizontal = ('secondary_activities',)
    readonly_fields = ('created_at', 'updated_at')
