from django.db import models

class FAQCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome da Categoria")
    order = models.PositiveIntegerField(default=0, help_text="Define a ordem de exibição das categorias.")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoria de FAQ"
        verbose_name_plural = "Categorias de FAQ"
        ordering = ['order']


class FAQItem(models.Model):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='questions', verbose_name="Categoria")
    question = models.CharField(max_length=255, verbose_name="Pergunta")
    answer = models.TextField(verbose_name="Resposta")
    order = models.PositiveIntegerField(default=0, help_text="Define a ordem de exibição das perguntas dentro de uma categoria.")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Pergunta Frequente"
        verbose_name_plural = "Perguntas Frequentes"
        ordering = ['order']