# user_management/views.py

import json
import random
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
# CORREÇÃO: Importando timezone da maneira correta
from django.utils import timezone

from .forms import (BusinessUserCreationForm, EducationalUserCreationForm,
                    UserChangeRequestForm)
from .models import CustomUser, UserChangeRequest


def home_page(request):
    cards = [
        {'title': "Inteligência de Mercado", 'url': 'intelligence_market:indicator_list'},
        {'title': "Acordos e Regulamentos", 'url': '#'},
        {'title': "Oportunidades", 'url': '#'},
        {'title': "Aprenda Comex", 'url': 'learning_management:apreda_comex_landing'},
        {'title': "Destino Roraima", 'url': '#'},
        {'title': "Notícias", 'url': '#'},
    ]
    context = {
        'cards': cards,
    }
    return render(request, 'home.html', context)

def vender_landing(request):
    return render(request, 'user_management/vender_landing.html')

def register_business_qualify(request):
    if request.method == 'POST':
        situation = request.POST.get('situation')
        if situation == 'formalized':
            return redirect('user_management:register_business_create')
        elif situation == 'informal':
            return render(request, 'user_management/consultancy_placeholder.html')
        else:
            return render(request, 'user_management/register_business_qualify.html', {'error': 'Por favor, selecione uma opção.'})
            
    return render(request, 'user_management/register_business_qualify.html')

def create_business_account(request):
    if request.method == 'POST':
        form = BusinessUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            try:
                send_mail(
                    'Seu Código de Verificação - Roraima Trade Hub',
                    f'Olá! Seu código de verificação é: {user.verification_code}',
                    'nao-responda@roraimatradehub.com',
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Conta pré-cadastrada! Enviamos um código de verificação para o seu e-mail.')
                return redirect(reverse('user_management:verify_email') + f'?email={user.email}')
            except Exception as e:
                messages.error(request, 'Houve um problema ao enviar o e-mail de verificação. Tente novamente.')
                user.delete()
                # Retorna para o formulário em branco em caso de falha no e-mail
                return redirect('user_management:register_business_create')

    # CORREÇÃO: A lógica foi ajustada aqui.
    # Se o método NÃO for POST (ou seja, é o primeiro acesso)
    # OU se o formulário do POST for inválido, ele chegará aqui.
    else:
        form = BusinessUserCreationForm()
    
    # Renderiza a página com o formulário (seja ele em branco ou com os erros de validação)
    return render(request, 'user_management/register_business.html', {'form': form})

def consultancy_placeholder(request):
    return render(request, 'base.html')

def register_educational(request):
    # ... (código existente, sem alterações) ...
    if request.method == 'POST':
        form = EducationalUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Conta criada com sucesso para {user.full_name}! Você já pode fazer o login.')
            return redirect('user_management:login')
    else:
        form = EducationalUserCreationForm()
    
    return render(request, 'user_management/register_educational.html', {'form': form})

def verify_email(request):
    # ... (código existente, sem alterações) ...
    email = request.GET.get('email') or request.POST.get('email')
    if not email:
        messages.error(request, 'E-mail não fornecido. Por favor, comece o cadastro novamente.')
        return redirect('user_management:register_business')

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        messages.error(request, 'Usuário não encontrado. Por favor, realize o cadastro.')
        return redirect('user_management:register_business')

    if user.is_active:
        messages.info(request, 'Esta conta já foi ativada. Você pode fazer o login.')
        return redirect('user_management:login')

    if request.method == 'POST':
        code = request.POST.get('code')
        if not code:
            messages.error(request, 'Por favor, insira o código de verificação.')
        elif user.verification_code != code:
            messages.error(request, 'Código de verificação inválido.')
        elif timezone.now() > user.verification_code_expires_at:
            messages.error(request, 'Código de verificação expirado. Por favor, solicite um novo.')
        else:
            user.is_active = True
            user.email_verified = True
            user.verification_code = None
            user.verification_code_expires_at = None
            user.save()
            messages.success(request, 'E-mail verificado com sucesso! Sua conta está ativa e você já pode fazer login.')
            return redirect('user_management:login')

    return render(request, 'user_management/verify_email.html', {'email': email})

@login_required
def dashboard(request):
    # ... (código existente, sem alterações) ...
    user = request.user
    if user.user_type == 'BUSINESS':
        return render(request, 'user_management/dashboard.html')
    elif user.user_type == 'EDUCATIONAL':
        return redirect('learning_management:educational_dashboard')
    else:
        return redirect('home')

@login_required
def user_profile(request):
    # ... (código existente, sem alterações) ...
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