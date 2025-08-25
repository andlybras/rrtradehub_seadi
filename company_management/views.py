from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CompanyCreationForm

@login_required
def register_company(request):
    if request.method == 'POST':
        form = CompanyCreationForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            # O save_m2m() é necessário para salvar os campos ManyToManyField
            form.save_m2m()
            messages.success(request, 'Sua empresa foi cadastrada com sucesso e enviada para análise!')
            return redirect('user_management:dashboard')
    else:
        form = CompanyCreationForm()

    return render(request, 'register_company.html', {'form': form})
