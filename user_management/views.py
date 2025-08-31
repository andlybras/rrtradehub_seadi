from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BusinessUserCreationForm, UserChangeRequestForm, EducationalUserCreationForm, timezone
from .models import UserChangeRequest, CustomUser
import json
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse

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
            # Redireciona para a URL do formulário de criação de conta
            return redirect('user_management:register_business_create')
        elif situation == 'informal':
            # Redireciona para uma página de placeholder para a consultoria
            return render(request, 'user_management/consultancy_placeholder.html')
        else:
            # Caso o usuário não selecione nada e clique em "Continuar"
            return render(request, 'user_management/register_business_qualify.html', {'error': 'Por favor, selecione uma opção.'})
            
    return render(request, 'user_management/register_business_qualify.html')

# VIEW RENOMEADA para o formulário de criação de conta
def create_business_account(request):
    if request.method == 'POST':
        form = BusinessUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Lógica de envio de e-mail
            try:
                send_mail(
                    'Seu Código de Verificação - Roraima Trade Hub',
                    f'Olá! Seu código de verificação é: {user.verification_code}',
                    'nao-responda@roraimatradehub.com', # Substitua pelo seu e-mail
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Conta pré-cadastrada! Enviamos um código de verificação para o seu e-mail.')
                # Redireciona para a nova página de verificação (que criaremos a seguir)
                return redirect(reverse('user_management:verify_email') + f'?email={user.email}')
            except Exception as e:
                # Se o e-mail falhar, podemos avisar o usuário
                messages.error(request, 'Houve um problema ao enviar o e-mail de verificação. Tente novamente.')
                user.delete() # Remove o usuário pré-cadastrado para evitar lixo no banco
    else:
        form = BusinessUserCreationForm()
    
    return render(request, 'user_management/register_business.html', {'form': form})
# NOVA PÁGINA (em branco por enquanto)
def consultancy_placeholder(request):
    return render(request, 'base.html') # Apenas renderiza a base por enquanto

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

def verify_email(request):
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
            # Aqui poderíamos adicionar a lógica para reenviar o código
        else:
            user.is_active = True
            user.email_verified = True
            user.verification_code = None # Limpamos o código após o uso
            user.verification_code_expires_at = None
            user.save()
            messages.success(request, 'E-mail verificado com sucesso! Sua conta está ativa e você já pode fazer login.')
            return redirect('user_management:login')

    return render(request, 'user_management/verify_email.html', {'email': email})

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
