# learning_management/views.py

from django.shortcuts import render

def aprenda_comex_landing(request):
    """
    Exibe a página de apresentação do módulo Aprenda Comex.
    """
    return render(request, 'learning_management/apreda_comex_landing.html')