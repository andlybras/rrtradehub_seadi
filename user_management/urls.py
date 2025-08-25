from django.urls import path
from . import views

app_name = 'user_management'

urlpatterns = [
    path('registro-empresarial/', views.register_business, name='register_business'),
]