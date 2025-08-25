from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import ModelForm, MultipleChoiceField, CheckboxSelectMultiple
from django.apps import apps
from .models import CustomUser, AppModulePermission, UserChangeRequest
import json

class AppModulePermissionAdminForm(ModelForm):
    class Meta:
        model = AppModulePermission
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app_labels = [app.label for app in apps.get_app_configs() if 'django.contrib' not in app.name and app.name != 'config']
        choices = [(label, label) for label in app_labels]
        self.fields['responsible_modules'] = MultipleChoiceField(choices=choices, widget=CheckboxSelectMultiple, label='Módulo(s) de Responsabilidade', required=False)
        if self.instance.pk:
            self.initial['responsible_modules'] = self.instance.get_responsible_modules_list()

    def save(self, commit=True):
        self.instance.responsible_modules = ','.join(self.cleaned_data.get('responsible_modules', []))
        return super().save(commit=commit)

@admin.register(AppModulePermission)
class AppModulePermissionAdmin(admin.ModelAdmin):
    form = AppModulePermissionAdminForm
    list_display = ('name', 'responsible_modules')
    search_fields = ('name',)
    filter_horizontal = ('users',)

    def has_module_permission(self, request):
        return request.user.is_superuser

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'nome_fantasia', 'user_type', 'is_staff')
    search_fields = ('username', 'email', 'nome_fantasia', 'cnpj')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Principais', {'fields': ('email', 'user_type')}),
        ('Dados do Perfil Empresarial', {'fields': ('razao_social', 'nome_fantasia', 'cnpj'), 'classes': ('collapse', 'business-fields')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js', 'js/admin_user_toggle.js',)

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if getattr(request.user, 'user_type', None) == 'LICENSEE' and request.user.is_staff:
            assigned_modules = set()
            for perm in request.user.app_permissions.all():
                assigned_modules.update(perm.get_responsible_modules_list())
            return 'user_management' in assigned_modules
        return False

@admin.register(UserChangeRequest)
class UserChangeRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username',)
    readonly_fields = ('user', 'requested_changes', 'created_at', 'moderated_at')
    actions = ['approve_user_changes', 'reject_user_changes']

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if getattr(request.user, 'user_type', None) == 'LICENSEE' and request.user.is_staff:
            assigned_modules = set()
            for perm in request.user.app_permissions.all():
                assigned_modules.update(perm.get_responsible_modules_list())
            return 'user_management' in assigned_modules
        return False

    @admin.action(description='Aprovar alterações de dados de usuário')
    def approve_user_changes(self, request, queryset):
        for req in queryset.filter(status=UserChangeRequest.Status.PENDING):
            user = req.user
            try:
                changes = json.loads(req.requested_changes)
                for field, value in changes.items():
                    if hasattr(user, field):
                        setattr(user, field, value)
                user.save()
                req.status = UserChangeRequest.Status.APPROVED
                req.save()
            except json.JSONDecodeError:
                 self.message_user(request, f'Erro ao processar a solicitação para {user.username}.', messages.ERROR)
        self.message_user(request, f'{queryset.count()} solicitações foram aprovadas.', messages.SUCCESS)

    @admin.action(description='Rejeitar alterações de dados de usuário')
    def reject_user_changes(self, request, queryset):
        updated = queryset.filter(status=UserChangeRequest.Status.PENDING).update(status=UserChangeRequest.Status.REJECTED)
        self.message_user(request, f'{updated} solicitações foram rejeitadas.', messages.WARNING)
