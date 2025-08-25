from django.contrib import admin
from django.urls import path, include
from user_management import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home_page, name='home'),
    path('contas/', include('user_management.urls')),
    path('empresa/', include('company_management.urls')),
    path('painel/', include('showcase_management.urls')), # Adicione esta linha
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
