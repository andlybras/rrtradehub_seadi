# config/urls.py

from django.contrib import admin
from django.urls import path, include
from user_management import views as user_views # Mantenha esta importação
from django.conf import settings
from django.conf.urls.static import static

# --- NOVO ---
# Vamos agrupar todas as URLs da plataforma principal aqui.
plataforma_patterns = [
    # A antiga página inicial agora é a raiz deste grupo
    path('', user_views.home_page, name='home'), 
    
    # As outras URLs continuam como estavam
    path('contas/', include('user_management.urls')),
    path('empresa/', include('company_management.urls')),
    path('painel/', include('showcase_management.urls')),
    path('quero-comprar/', include('showcase_management.public_urls')),
    path('suporte/', include('support_management.urls')),
    path('inteligencia/', include('intelligence_market.urls')),
    path('', include('learning_management.urls')),
]
# --- FIM DO NOVO BLOCO ---


urlpatterns = [
    # A área de admin continua separada e no mesmo lugar
    path('admin/', admin.site.urls),

    # --- ALTERADO ---
    # 1. A rota principal '/' agora aponta para a nossa nova página de recepção
    path('', include('core.urls', namespace='core')),

    # 2. Todas as URLs da plataforma agora estão organizadas sob o prefixo '/plataforma/'
    path('plataforma/', include(plataforma_patterns)),
    # --- FIM DA ALTERAÇÃO ---
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)