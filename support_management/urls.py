# support_management/urls.py
from django.urls import path
from . import views

app_name = 'support_management'

urlpatterns = [
    path('faq/', views.faq_page, name='faq_page'),
]