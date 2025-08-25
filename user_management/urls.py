from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'user_management'

urlpatterns = [
    path('registro-empresarial/', views.register_business, name='register_business'),
    path('login/', auth_views.LoginView.as_view(template_name='user_management/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('painel/', views.dashboard, name='dashboard'),
]