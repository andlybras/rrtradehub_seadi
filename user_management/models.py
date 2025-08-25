from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    class UserType(models.TextChoices):
        LICENSEE = 'LICENSEE', 'Permissionário'
        BUSINESS = 'BUSINESS', 'Perfil Empresarial'

    user_type = models.CharField(max_length=10, choices=UserType.choices, verbose_name='Tipo de Usuário')
    razao_social = models.CharField(max_length=255, blank=True, null=True, verbose_name='Razão Social')
    nome_fantasia = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nome Fantasia')
    cnpj = models.CharField(max_length=18, blank=True, null=True, unique=True, verbose_name='CNPJ')

    def __str__(self):
        return self.username

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
