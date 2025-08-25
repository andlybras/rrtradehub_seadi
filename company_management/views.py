from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CompanyCreationForm, CompanyChangeRequestForm
from .models import Company, CNAE, ChangeRequest
import json

@login_required
def company_details(request):
    try:
        company = request.user.company
    except Company.DoesNotExist:
        company = None

    edit_mode = 'edit' in request.GET and company and company.status == 'ACTIVE'

    if request.method == 'POST':
        if not company:
            form = CompanyCreationForm(request.POST, request.FILES)
            if form.is_valid():
                new_company = form.save(commit=False)
                new_company.owner = request.user
                new_company.save()
                form.save_m2m()
                messages.success(request, 'Sua empresa foi cadastrada e enviada para análise!')
                return redirect('user_management:dashboard')
        elif edit_mode:
            form = CompanyChangeRequestForm(request.POST, request.FILES, instance=company)
            if form.is_valid():
                changed_data = {f: form.cleaned_data[f] for f in form.changed_data}
                if 'logo' in changed_data and changed_data['logo'] is False:
                    del changed_data['logo']
                
                if changed_data:
                    ChangeRequest.objects.create(
                        company=company,
                        requested_by=request.user,
                        requested_changes=json.dumps(changed_data, default=str)
                    )
                    company.status = 'REVIEW'
                    company.save()
                    messages.success(request, 'Sua solicitação de alteração foi enviada para análise.')
                else:
                    messages.info(request, 'Nenhuma alteração foi detectada.')
                return redirect('company_management:company_details')
    else:
        if not company:
            form = CompanyCreationForm(initial={'razao_social': request.user.razao_social, 'nome_fantasia': request.user.nome_fantasia, 'cnpj': request.user.cnpj})
        else:
            form = CompanyChangeRequestForm(instance=company) if edit_mode else None

    cnae_options = list(CNAE.objects.values('id', 'code', 'description'))
    context = {
        'form': form,
        'company': company,
        'edit_mode': edit_mode,
        'cnae_options_json': json.dumps(cnae_options)
    }
    return render(request, 'company_management/company_details.html', context)