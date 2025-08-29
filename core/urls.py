# core/urls.py
from django.urls import path
from .views import reception_view

app_name = 'core'

urlpatterns = [
    path('', reception_view, name='reception'),
]