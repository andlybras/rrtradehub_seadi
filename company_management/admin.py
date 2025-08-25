from django.contrib import admin, messages
from .models import CNAE, Company, ChangeRequest

@admin.register(CNAE)
class CNAEAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')

class ChangeRequestInline(admin.TabularInline):
    model = ChangeRequest
    extra = 0
    fields = ('requested_by', 'status', 'created_at')
    readonly_fields = ('requested_by', 'created_at')
    can_delete = False

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'owner', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('nome_fantasia', 'razao_social', 'cnpj', 'owner__username')
    
    fieldsets = (
        ('Dados do Proprietário', {'fields': ('owner',)}),
        ('Dados Empresariais', {'fields': ('razao_social', 'nome_fantasia', 'cnpj', 'inscricao_estadual', 'main_activity', 'secondary_activities', 'logo')}),
        ('Informações de Contato', {'fields': ('institutional_contact', 'institutional_email', 'address')}),
        ('Dados do Responsável Legal', {'fields': ('legal_rep_name', 'legal_rep_role', 'legal_rep_contact', 'legal_rep_email')}),
        ('Moderação', {'fields': ('status', 'moderation_notes')}),
    )
    filter_horizontal = ('secondary_activities',)
    readonly_fields = ('created_at', 'updated_at', 'owner')
    inlines = [ChangeRequestInline]
    
    actions = ['approve_companies']

    @admin.action(description='Aprovar empresas selecionadas')
    def approve_companies(self, request, queryset):
        updated = queryset.update(status=Company.Status.ACTIVE)
        self.message_user(request, f'{updated} empresas foram aprovadas com sucesso.', messages.SUCCESS)

@admin.register(ChangeRequest)
class ChangeRequestAdmin(admin.ModelAdmin):
    list_display = ('company', 'requested_by', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('company__nome_fantasia', 'requested_by__username')
    readonly_fields = ('company', 'requested_by', 'requested_changes', 'created_at', 'moderated_at')
