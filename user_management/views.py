from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BusinessUserCreationForm, UserChangeRequestForm
from .models import UserChangeRequest
import json

def home_page(request):
    card_titles = [
        "Inteligência de Mercado", "Acordos e Regulamentos", "Oportunidades",
        "Aprenda Comex", "Destino Roraima", "Notícias"
    ]
    context = {
        'titulo_da_pagina': 'Bem-vindo ao nosso site!',
        'card_titles': card_titles,
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
    
    return render(request, 'user_management/register_business.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'user_management/dashboard.html')

@login_required
def user_profile(request):
    user = request.user
    edit_mode = 'edit' in request.GET

    if request.method == 'POST' and edit_mode:
        form = UserChangeRequestForm(request.POST, instance=user)
        if form.is_valid():
            if form.changed_data:
                changed_data = {f: form.cleaned_data[f] for f in form.changed_data}
                UserChangeRequest.objects.create(
                    user=user,
                    requested_changes=json.dumps(changed_data, default=str)
                )
                messages.success(request, 'Sua solicitação de alteração de dados foi enviada para análise.')
            else:
                messages.info(request, 'Nenhuma alteração foi detectada.')
            return redirect('user_management:user_profile')
    else:
        form = UserChangeRequestForm(instance=user) if edit_mode else None

    context = {
        'form': form,
        'edit_mode': edit_mode
    }
    return render(request, 'user_management/user_profile.html', context)
