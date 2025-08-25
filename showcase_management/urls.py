from django.urls import path
from . import views

app_name = 'showcase_management'

urlpatterns = [
    path('vitrine/', views.product_list, name='product_list'),
    path('vitrine/adicionar/', views.product_create, name='product_create'),
    path('vitrine/editar/<int:pk>/', views.product_update, name='product_update'),
    path('vitrine/excluir/<int:pk>/', views.product_delete, name='product_delete'),
]
