from django import forms
from .models import Company, CNAE

class CompanyCreationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'razao_social', 'nome_fantasia', 'cnpj', 'inscricao_estadual',
            'main_activity', 'secondary_activities', 'institutional_contact',
            'institutional_email', 'address', 'logo', 'legal_rep_name',
            'legal_rep_role', 'legal_rep_contact', 'legal_rep_email'
        ]
        widgets = {
            'razao_social': forms.TextInput(attrs={'class': 'form-input-readonly', 'readonly': True}),
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-input-readonly', 'readonly': True}),
            'cnpj': forms.TextInput(attrs={'class': 'form-input-readonly', 'readonly': True}),
            'inscricao_estadual': forms.TextInput(attrs={'class': 'form-input'}),
            'institutional_contact': forms.TextInput(attrs={'class': 'form-input'}),
            'institutional_email': forms.EmailInput(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'legal_rep_name': forms.TextInput(attrs={'class': 'form-input'}),
            'legal_rep_role': forms.TextInput(attrs={'class': 'form-input'}),
            'legal_rep_contact': forms.TextInput(attrs={'class': 'form-input'}),
            'legal_rep_email': forms.EmailInput(attrs={'class': 'form-input'}),
            'main_activity': forms.HiddenInput(),
            'secondary_activities': forms.MultipleHiddenInput(),
        }

class CompanyChangeRequestForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'inscricao_estadual', 'main_activity', 'secondary_activities', 
            'institutional_contact', 'institutional_email', 'address', 'logo', 
            'legal_rep_name', 'legal_rep_role', 'legal_rep_contact', 'legal_rep_email'
        ]
        widgets = {
            'inscricao_estadual': forms.TextInput(attrs={'class': 'form-input'}),
            'institutional_contact': forms.TextInput(attrs={'class': 'form-input'}),
            'institutional_email': forms.EmailInput(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'legal_rep_name': forms.TextInput(attrs={'class': 'form-input'}),
            'legal_rep_role': forms.TextInput(attrs={'class': 'form-input'}),
            'legal_rep_contact': forms.TextInput(attrs={'class': 'form-input'}),
            'legal_rep_email': forms.EmailInput(attrs={'class': 'form-input'}),
            'main_activity': forms.HiddenInput(),
            'secondary_activities': forms.MultipleHiddenInput(),
        }
