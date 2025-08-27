from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BusinessUserCreationForm, UserChangeRequestForm, EducationalUserCreationForm
from .models import UserChangeRequest
import json

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

def register_educational(request):
    if request.method == 'POST':
        form = EducationalUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Conta criada com sucesso para {user.full_name}! Você já pode fazer o login.')
            return redirect('user_management:login') # Redireciona para o login
    else:
        form = EducationalUserCreationForm()
    
    return render(request, 'user_management/register_educational.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    if user.user_type == 'BUSINESS':
        # Mantém o comportamento atual para usuários empresariais
        return render(request, 'user_management/dashboard.html')
    elif user.user_type == 'EDUCATIONAL':
        # Redireciona para o novo painel educacional
        return redirect('learning_management:educational_dashboard')
    else:
        # Você pode adicionar um comportamento padrão ou uma página de erro aqui
        # Por enquanto, vamos redirecionar para a home
        return redirect('home')

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
