from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.apps import apps
from django import forms

class CustomUser(AbstractUser):
    class UserType(models.TextChoices):
        LICENSEE = 'LICENSEE', 'Permissionário'
        BUSINESS = 'BUSINESS', 'Perfil Empresarial'
        EDUCATIONAL = 'EDUCATIONAL', 'Perfil Educacional'

    class EducationLevel(models.TextChoices):
        ENSINO_FUNDAMENTAL = 'FUNDAMENTAL', 'Ensino Fundamental'
        ENSINO_MEDIO = 'MEDIO', 'Ensino Médio'
        ENSINO_SUPERIOR = 'SUPERIOR', 'Ensino Superior'
        POS_GRADUACAO = 'POS_GRADUACAO', 'Pós-Graduação'
        OUTRO = 'OUTRO', 'Outro'
        
    user_type = models.CharField(max_length=11, choices=UserType.choices, verbose_name='Tipo de Usuário')
    razao_social = models.CharField(max_length=255, blank=True, null=True, verbose_name='Razão Social')
    nome_fantasia = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nome Fantasia')
    cnpj = models.CharField(max_length=18, blank=True, null=True, unique=True, verbose_name='CNPJ')
    
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nome Completo')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Data de Nascimento')
    education_level = models.CharField(
        max_length=20,
        choices=EducationLevel.choices,
        blank=True,
        null=True,
        verbose_name='Escolaridade'
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Salva o usuário primeiro para garantir que ele tenha um ID
        super().save(*args, **kwargs)

        # Se for um Permissionário, sincroniza as permissões
        if self.user_type == self.UserType.LICENSEE and self.is_staff:
            self.user_permissions.clear()
            permissions_to_add = set()
            
            for app_permission_group in self.app_permissions.all():
                for module_name in app_permission_group.get_responsible_modules_list():
                    try:
                        app_models = apps.get_app_config(module_name).get_models()
                        for model in app_models:
                            content_type = ContentType.objects.get_for_model(model)
                            permissions = Permission.objects.filter(content_type=content_type)
                            permissions_to_add.update(permissions)
                    except (LookupError, AttributeError):
                        continue # Ignora se o app não for encontrado
            
            if permissions_to_add:
                self.user_permissions.add(*permissions_to_add)

class UserChangeRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendente'
        APPROVED = 'APPROVED', 'Aprovada'
        REJECTED = 'REJECTED', 'Rejeitada'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='change_requests', verbose_name='Usuário')
    requested_changes = models.JSONField(verbose_name='Dados Solicitados')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, verbose_name='Status da Solicitação')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data da Solicitação')
    moderated_at = models.DateTimeField(null=True, blank=True, verbose_name='Data da Moderação')
    moderator_notes = models.TextField(blank=True, null=True, verbose_name='Notas do Moderador')

    def __str__(self):
        return f"Solicitação de {self.user.username} em {self.created_at.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = 'Solicitação de Alteração de Usuário'
        verbose_name_plural = 'Solicitações de Alteração de Usuários'

class AppModulePermission(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nome da Permissão')
    responsible_modules = models.CharField(max_length=255, blank=True, verbose_name='Módulo(s) de Responsabilidade', help_text='Nomes dos apps do projeto separados por vírgula (ex: company_management, user_management)')
    users = models.ManyToManyField(CustomUser, related_name='app_permissions', blank=True, limit_choices_to={'user_type': CustomUser.UserType.LICENSEE}, verbose_name='Permissionários Vinculados')

    def get_responsible_modules_list(self):
        if not self.responsible_modules:
            return []
        return [module.strip() for module in self.responsible_modules.split(',')]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Permissão de Módulo'
        verbose_name_plural = 'Gerenciamento de Permissões'
