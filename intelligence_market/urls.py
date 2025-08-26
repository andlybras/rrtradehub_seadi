from django.urls import path
from . import views

app_name = 'intelligence_market'

urlpatterns = [
    # Rota para a lista de cards -> chama a view indicator_list_view
    path('', views.indicator_list_view, name='indicator_list'),
    
    # Rota para a página de detalhe -> chama a view indicator_detail_view
    path('pagina/<int:pk>/', views.indicator_detail_view, name='indicator_detail'),
]