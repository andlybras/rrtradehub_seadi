from django.contrib import admin
from django.urls import path, include
from user_management import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

plataforma_patterns = [
    path('', user_views.home_page, name='home'), 
    path('contas/', include('user_management.urls')),
    path('empresa/', include('company_management.urls')),
    path('painel/', include('showcase_management.urls')),
    path('quero-comprar/', include('showcase_management.public_urls')),
    path('suporte/', include('support_management.urls')),
    path('inteligencia/', include('intelligence_market.urls')),
    path('', include('learning_management.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
]

urlpatterns += i18n_patterns(
    path('plataforma/', include(plataforma_patterns)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)