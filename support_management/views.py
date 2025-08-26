from django.shortcuts import render
from .models import FAQCategory

def faq_page(request):
    # Buscamos todas as categorias. Graças ao 'related_name' no model,
    # cada categoria já virá com suas respectivas perguntas ('questions') associadas.
    categories = FAQCategory.objects.prefetch_related('questions').all()
    context = {
        'categories': categories
    }
    return render(request, 'support_management/faq_page.html', context)