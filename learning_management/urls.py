# learning_management/urls.py

from django.urls import path
from . import views

app_name = 'learning_management'

urlpatterns = [
    path('aprenda-comex/', views.aprenda_comex_landing, name='apreda_comex_landing'),
]