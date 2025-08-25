from django.db import models
from django.conf import settings

class CNAE(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name='Código CNAE')
    description = models.TextField(verbose_name='Descrição')

    def __str__(self):
        return f'{self.code} - {self.description}'

    class Meta:
        verbose_name = 'CNAE'
        verbose_name_plural = 'Gerenciamento de CNAEs'


class Company(models.Model):
    class Status(models.TextChoices):
        REVIEW = 'REVIEW', 'Em Análise'
        ACTIVE = 'ACTIVE', 'Ativa'
        REJECTED = 'REJECTED', 'Recusada'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='companies',
        verbose_name='Proprietário (Perfil Empresarial)',
        limit_choices_to={'user_type': 'BUSINESS'}
    )
    razao_social = models.CharField(max_length=255, verbose_name='Razão Social')
    nome_fantasia = models.CharField(max_length=255, verbose_name='Nome Fantasia')
    cnpj = models.CharField(max_length=18, unique=True, verbose_name='CNPJ')
    inscricao_estadual = models.CharField(max_length=20, blank=True, null=True, verbose_name='Inscrição Estadual')
    
    main_activity = models.ForeignKey(
        CNAE,
        on_delete=models.SET_NULL,
        null=True,
        related_name='main_activity_companies',
        verbose_name='Atividade Principal (CNAE)'
    )
    secondary_activities = models.ManyToManyField(
        CNAE,
        related_name='secondary_activity_companies',
        blank=True,
        verbose_name='Atividades Secundárias (CNAE)'
    )
    
    institutional_contact = models.CharField(max_length=20, blank=True, null=True, verbose_name='Contato Institucional')
    institutional_email = models.EmailField(blank=True, null=True, verbose_name='E-mail Institucional')
    address = models.TextField(verbose_name='Endereço Principal')
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True, verbose_name='Logotipo')
    legal_rep_name = models.CharField(max_length=255, verbose_name='Nome Completo do Responsável')
    legal_rep_role = models.CharField(max_length=100, verbose_name='Cargo/Função')
    legal_rep_contact = models.CharField(max_length=20, verbose_name='Contato Direto/WhatsApp')
    legal_rep_email = models.EmailField(verbose_name='Email do Responsável')
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.REVIEW,
        verbose_name='Status'
    )
    moderation_notes = models.TextField(blank=True, null=True, verbose_name='Justificativa/Notas de Moderação')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome_fantasia

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Gerenciamento de Empresas'
