from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, ProductImage, NCMSubitem, NCMChapter, NCMPosition, Company
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

def search_page(request):
    # Filtra apenas capítulos que têm produtos ativos de empresas ativas
    active_chapters = NCMChapter.objects.filter(
        positions__subitems__products__is_active=True,
        positions__subitems__products__company__status=Company.Status.ACTIVE
    ).distinct()
    
    context = {
        'chapters': active_chapters,
    }
    return render(request, 'showcase_management/search_page.html', context)

def search_results(request):
    product_id = request.GET.get('product')
    if not product_id:
        return redirect('showcase_public:search_page')

    product = get_object_or_404(Product, pk=product_id)
    # Encontra todas as empresas ativas que vendem este produto
    companies = Company.objects.filter(
        status=Company.Status.ACTIVE,
        products__id=product_id
    ).distinct()

    context = {
        'product': product,
        'companies': companies,
    }
    return render(request, 'showcase_management/search_results.html', context)

def public_company_profile(request, pk):
    company = get_object_or_404(Company, pk=pk, status=Company.Status.ACTIVE)
    highlight_product_id = request.GET.get('produto')
    
    context = {
        'company': company,
        'highlight_product_id': int(highlight_product_id) if highlight_product_id else None,
    }
    return render(request, 'showcase_management/public_company_profile.html', context)

# --- Endpoints para AJAX ---

def load_positions(request):
    chapter_id = request.GET.get('chapter_id')
    # Filtra posições que têm produtos ativos de empresas ativas
    positions = list(NCMPosition.objects.filter(
        chapter_id=chapter_id,
        subitems__products__is_active=True,
        subitems__products__company__status=Company.Status.ACTIVE
    ).distinct().values('id', 'code', 'description'))
    return JsonResponse(positions, safe=False)

def load_products(request):
    position_id = request.GET.get('position_id')
    # Filtra produtos ativos de empresas ativas
    products = list(Product.objects.filter(
        ncm_subitem__position_id=position_id,
        is_active=True,
        company__status=Company.Status.ACTIVE
    ).distinct().values('id', 'title'))
    return JsonResponse(products, safe=False)