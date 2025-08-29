# core/views.py
from django.shortcuts import render

def reception_view(request):
    """
    Esta view apenas renderiza a nossa página de recepção.
    """
    return render(request, 'core/reception.html')