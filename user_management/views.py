from django.shortcuts import render

def home_page(request):
    context = {
        'titulo_da_pagina': 'Bem-vindo ao nosso site!',
    }
    return render(request, 'home.html', context)
