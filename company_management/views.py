from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CompanyCreationForm
from .models import CNAE
import json

@login_required
def register_company(request):
    if hasattr(request.user, 'companies') and request.user.companies.exists():
        messages.warning(request, 'Você já possui uma empresa cadastrada ou em análise.')
        return redirect('user_management:dashboard')

    if request.method == 'POST':
        form = CompanyCreationForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.razao_social = request.user.razao_social
            company.nome_fantasia = request.user.nome_fantasia
            company.cnpj = request.user.cnpj
            company.save()
            form.save_m2m()
            messages.success(request, 'Sua empresa foi cadastrada com sucesso e enviada para análise!')
            return redirect('user_management:dashboard')
    else:
        initial_data = {
            'razao_social': request.user.razao_social,
            'nome_fantasia': request.user.nome_fantasia,
            'cnpj': request.user.cnpj,
        }
        form = CompanyCreationForm(initial=initial_data)

    cnae_options = list(CNAE.objects.values('id', 'code', 'description'))

    context = {
        'form': form,
        'cnae_options_json': json.dumps(cnae_options)
    }
    return render(request, 'register_company.html', context)
