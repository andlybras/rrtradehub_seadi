from django.urls import path
from . import views

app_name = 'company_management'

urlpatterns = [
    path('cadastrar/', views.register_company, name='register_company'),
]
