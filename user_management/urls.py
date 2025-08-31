from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'user_management'

urlpatterns = [
    path('quero-vender/', views.vender_landing, name='vender_landing'),
    path('registro-empresarial/', views.register_business_qualify, name='register_business'),
    path('registro-empresarial/novo/', views.create_business_account, name='register_business_create'),
    path('verificar-email/', views.verify_email, name='verify_email'),
    path('registro-educacional/', views.register_educational, name='register_educational'),
    path('login/', auth_views.LoginView.as_view(template_name='user_management/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('painel/', views.dashboard, name='dashboard'),
    path('perfil/', views.user_profile, name='user_profile'),
]
