# learning_management/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def aprenda_comex_landing(request):
    """
    Exibe a página de apresentação do módulo Aprenda Comex.
    """
    return render(request, 'learning_management/apreda_comex_landing.html')

@login_required
def educational_dashboard(request):
    return render(request, 'learning_management/educational_dashboard.html')