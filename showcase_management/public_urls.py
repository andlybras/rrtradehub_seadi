from django.urls import path
from . import views

app_name = 'showcase_public'

urlpatterns = [
    path('', views.search_page, name='search_page'),
    path('resultados/', views.search_results, name='search_results'),
    path('empresa/<int:pk>/', views.public_company_profile, name='public_company_profile'),
    
    # URLs para a busca dinâmica (AJAX)
    path('api/load-positions/', views.load_positions, name='ajax_load_positions'),
    path('api/load-products/', views.load_products, name='ajax_load_products'),
]
