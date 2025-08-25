from django.contrib import admin
from django.urls import path, include
from user_management import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home_page, name='home'),
    path('contas/', include('user_management.urls')),
]