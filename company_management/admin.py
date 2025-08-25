from django.contrib import admin, messages
from .models import CNAE, Company, ChangeRequest
import json

@admin.register(CNAE)
class CNAEAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if getattr(request.user, 'user_type', None) == 'LICENSEE' and request.user.is_staff:
            assigned_modules = set()
            for perm in request.user.app_permissions.all():
                assigned_modules.update(perm.get_responsible_modules_list())
            return 'company_management' in assigned_modules
        return False

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

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if getattr(request.user, 'user_type', None) == 'LICENSEE' and request.user.is_staff:
            assigned_modules = set()
            for perm in request.user.app_permissions.all():
                assigned_modules.update(perm.get_responsible_modules_list())
            return 'company_management' in assigned_modules
        return False

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
    actions = ['approve_change_requests', 'reject_change_requests']

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if getattr(request.user, 'user_type', None) == 'LICENSEE' and request.user.is_staff:
            assigned_modules = set()
            for perm in request.user.app_permissions.all():
                assigned_modules.update(perm.get_responsible_modules_list())
            return 'company_management' in assigned_modules
        return False

    @admin.action(description='Aprovar solicitações de alteração selecionadas')
    def approve_change_requests(self, request, queryset):
        for req in queryset.filter(status=ChangeRequest.Status.PENDING):
            company = req.company
            try:
                changes = json.loads(req.requested_changes)
                for field, value in changes.items():
                    if hasattr(company, field):
                        if field == 'secondary_activities':
                            company.secondary_activities.set(value)
                        else:
                            setattr(company, field, value)
                company.status = Company.Status.ACTIVE
                company.save()
                req.status = ChangeRequest.Status.APPROVED
                req.save()
            except json.JSONDecodeError:
                self.message_user(request, f'Erro ao processar a solicitação para {company.nome_fantasia}.', messages.ERROR)
        self.message_user(request, f'{queryset.count()} solicitações foram processadas com sucesso.', messages.SUCCESS)

    @admin.action(description='Rejeitar solicitações de alteração selecionadas')
    def reject_change_requests(self, request, queryset):
        for req in queryset.filter(status=ChangeRequest.Status.PENDING):
            company = req.company
            company.status = Company.Status.ACTIVE
            company.save()
            req.status = ChangeRequest.Status.REJECTED
            req.save()
        self.message_user(request, f'{queryset.count()} solicitações foram rejeitadas.', messages.WARNING)
