from django.db import models

class SiteAsset(models.Model):
    class AssetType(models.TextChoices):
        HEADER_LOGO_PLATFORM = 'LOGO_PLATAFORMA', 'Logo da Plataforma (Header)'
        HEADER_LOGO_GOV = 'LOGO_GOVERNO', 'Logo do Governo/Secretaria (Header)'
        PARTNER_LOGO = 'LOGO_PARCEIRO', 'Logo de Parceiro (Rodapé)'

    name = models.CharField(max_length=100, verbose_name="Nome/Descrição do Recurso")
    asset_type = models.CharField(
        max_length=20,
        choices=AssetType.choices,
        verbose_name="Tipo do Recurso"
    )
    image = models.ImageField(upload_to='site_assets/', verbose_name="Arquivo de Imagem")
    url_link = models.URLField(blank=True, null=True, verbose_name="Link (Opcional)")
    order = models.PositiveIntegerField(default=0, help_text="Define a ordem de exibição para parceiros.")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Recurso do Site"
        verbose_name_plural = "Recursos do Site"
        ordering = ['order']
