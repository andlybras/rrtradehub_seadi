from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Product, ProductImage, NCMSubitem
from .forms import ProductForm
import json

@login_required
def product_list(request):
    try:
        company = request.user.company
        products = Product.objects.filter(company=company)
    except AttributeError:
        products = []
        messages.warning(request, "Você precisa cadastrar os dados da sua empresa primeiro.")
        return redirect('company_management:company_details')

    return render(request, 'showcase_management/product_list.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        images = request.FILES.getlist('images')
        if form.is_valid() and len(images) > 0 and len(images) <= 3:
            product = form.save(commit=False)
            product.company = request.user.company
            product.save()
            for img in images:
                ProductImage.objects.create(product=product, image=img)
            messages.success(request, "Produto cadastrado com sucesso!")
            return redirect('showcase_management:product_list')
        else:
            if not images:
                messages.error(request, "Você precisa enviar pelo menos uma imagem.")
            if len(images) > 3:
                messages.error(request, "Você pode enviar no máximo 3 imagens.")
    else:
        form = ProductForm()

    ncm_options = list(NCMSubitem.objects.values('id', 'code', 'description'))
    context = {
        'form': form,
        'ncm_options_json': json.dumps(ncm_options)
    }
    return render(request, 'showcase_management/product_form.html', context)

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, company=request.user.company)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado com sucesso!")
            return redirect('showcase_management:product_list')
    else:
        form = ProductForm(instance=product)

    ncm_options = list(NCMSubitem.objects.values('id', 'code', 'description'))
    context = {
        'form': form,
        'product': product,
        'ncm_options_json': json.dumps(ncm_options)
    }
    return render(request, 'showcase_management/product_form.html', context)

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, company=request.user.company)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Produto excluído com sucesso.")
        return redirect('showcase_management:product_list')
    return render(request, 'showcase_management/product_confirm_delete.html', {'product': product})
