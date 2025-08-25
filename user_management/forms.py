from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class BusinessUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('razao_social', 'nome_fantasia', 'cnpj', 'username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = CustomUser.UserType.BUSINESS
        if commit:
            user.save()
        return user
