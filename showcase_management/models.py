from django.db import models
from django.conf import settings
from company_management.models import Company

class NCMChapter(models.Model):
    code = models.CharField(max_length=2, unique=True, verbose_name="Capítulo")
    description = models.CharField(max_length=255, verbose_name="Descrição")

    def __str__(self):
        return f"{self.code} - {self.description}"

class NCMPosition(models.Model):
    chapter = models.ForeignKey(NCMChapter, on_delete=models.CASCADE, related_name='positions', verbose_name="Capítulo")
    code = models.CharField(max_length=4, unique=True, verbose_name="Posição")
    description = models.CharField(max_length=255, verbose_name="Descrição")

    def __str__(self):
        return f"{self.code} - {self.description}"

class NCMSubitem(models.Model):
    position = models.ForeignKey(NCMPosition, on_delete=models.CASCADE, related_name='subitems', verbose_name="Posição")
    code = models.CharField(max_length=8, unique=True, verbose_name="Subitem")
    description = models.TextField(verbose_name="Descrição")

    def __str__(self):
        return f"{self.code} - {self.description}"

class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products', verbose_name="Empresa")
    title = models.CharField(max_length=200, verbose_name="Título do Produto")
    description = models.TextField(verbose_name="Descrição")
    ncm_subitem = models.ForeignKey(NCMSubitem, on_delete=models.PROTECT, related_name='products', verbose_name="NCM (Subitem)")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Produto")
    image = models.ImageField(upload_to='product_images/', verbose_name="Imagem")
    is_approved = models.BooleanField(default=None, null=True, blank=True, verbose_name="Aprovada")
    moderator_notes = models.TextField(blank=True, null=True, verbose_name="Notas do Moderador")

    def __str__(self):
        return f"Imagem para {self.product.title}"
