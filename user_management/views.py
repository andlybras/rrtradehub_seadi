from django.shortcuts import render, redirect
from .forms import BusinessUserCreationForm
from django.contrib import messages

def home_page(request):
    context = {
        'titulo_da_pagina': 'Bem-vindo ao nosso site!',
    }
    return render(request, 'home.html', context)

def register_business(request):
    if request.method == 'POST':
        form = BusinessUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada com sucesso para {username}! Você já pode fazer o login.')
            return redirect('home')
    else:
        form = BusinessUserCreationForm()
    
    return render(request, 'register_business.html', {'form': form})
