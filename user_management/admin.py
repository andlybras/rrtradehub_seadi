from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import ModelForm, CheckboxSelectMultiple
from django.apps import apps
from .models import CustomUser, AppModulePermission

class AppModulePermissionAdminForm(ModelForm):

    class Meta:
        model = AppModulePermission
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        app_labels = [
            app.label for app in apps.get_app_configs() 
            if 'django.contrib' not in app.name and app.name != 'config'
        ]
        choices = [(label, label) for label in app_labels]
        
        self.fields['responsible_modules'] = admin.widgets.forms.MultipleChoiceField(
            choices=choices,
            widget=CheckboxSelectMultiple,
            label='Módulo(s) de Responsabilidade',
            required=False
        )
        
        if self.instance.pk:
            initial_modules = self.instance.get_responsible_modules_list()
            self.initial['responsible_modules'] = initial_modules

    def save(self, commit=True):
        selected_modules = self.cleaned_data.get('responsible_modules', [])
        self.instance.responsible_modules = ','.join(selected_modules)
        return super().save(commit=commit)


@admin.register(AppModulePermission)
class AppModulePermissionAdmin(admin.ModelAdmin):
    form = AppModulePermissionAdminForm
    list_display = ('name', 'responsible_modules')
    search_fields = ('name',)
    filter_horizontal = ('users',)


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Tipo de Usuário e Status', {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser')}),
        ('Dados do Perfil Empresarial', {
            'fields': ('razao_social', 'nome_fantasia', 'cnpj'),
            'classes': ('collapse', 'business-fields')
        }),
        ('Permissões', {'fields': ('groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    list_display = ('username', 'email', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'cnpj')

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js', 'js/admin_user_toggle.js',)
