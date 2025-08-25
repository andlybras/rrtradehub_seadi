from django.urls import path
from . import views

app_name = 'company_management'

urlpatterns = [
    path('dados/', views.company_details, name='company_details'),
]
