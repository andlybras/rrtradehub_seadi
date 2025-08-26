from django.db import models
from django.utils.text import slugify

class AnalysisPage(models.Model):
    # ... (nenhuma mudança aqui) ...
    """
    Representa uma página de análise completa, com conteúdo textual e gráficos.
    """
    card_title = models.CharField(max_length=100, verbose_name="Título do Card")
    card_image = models.ImageField(upload_to='intelligence_cards/', verbose_name="Imagem do Card")
    
    title = models.CharField(max_length=200, verbose_name="Título Principal da Página")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Subtítulo")
    
    content = models.TextField(verbose_name="Conteúdo da Análise")
    
    is_published = models.BooleanField(default=False, verbose_name="Publicado")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Página de Análise"
        verbose_name_plural = "Páginas de Análise"
        ordering = ['-created_at']


class Chart(models.Model):
    """
    Armazena a definição de um gráfico ECharts (código de opções em JavaScript).
    """
    name = models.CharField(max_length=100, verbose_name="Nome Interno do Gráfico")
    slug = models.SlugField(unique=True, blank=True, help_text="Identificador único para o shortcode, gerado automaticamente.")
    
    # --- MUDANÇA PRINCIPAL AQUI ---
    # Trocamos JSONField por TextField e ajustamos os nomes e textos de ajuda.
    options_js = models.TextField(
        verbose_name="Opções de Configuração (Código JavaScript do ECharts)",
        help_text="Cole aqui o objeto 'option' diretamente do exemplo do ECharts. Ex: { title: { text: 'Meu Gráfico' }, ... }"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    def get_shortcode(self):
        """Retorna o shortcode para ser usado no texto."""
        return f"[chart:{self.slug}]"

    def save(self, *args, **kwargs):
        """Gera o slug automaticamente a partir do nome se ele não existir."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Gráfico"
        verbose_name_plural = "Gráficos"