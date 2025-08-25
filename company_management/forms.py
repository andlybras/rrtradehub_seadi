from django import forms
from .models import Company, CNAE

class CompanyCreationForm(forms.ModelForm):
    main_activity = forms.ModelChoiceField(
        queryset=CNAE.objects.all(),
        label="Atividade Principal (CNAE)",
        empty_label="Selecione uma atividade principal"
    )
    
    secondary_activities = forms.ModelMultipleChoiceField(
        queryset=CNAE.objects.all(),
        label="Atividades Secundárias (CNAE)",
        widget=forms.SelectMultiple(attrs={'size': '10'}),
        required=False
    )

    class Meta:
        model = Company
        fields = [
            'razao_social', 'nome_fantasia', 'cnpj', 'inscricao_estadual',
            'main_activity', 'secondary_activities', 'institutional_contact',
            'institutional_email', 'address', 'logo', 'legal_rep_name',
            'legal_rep_role', 'legal_rep_contact', 'legal_rep_email'
        ]
        labels = {
            'razao_social': 'Razão Social',
            'nome_fantasia': 'Nome Fantasia',
            'inscricao_estadual': 'Inscrição Estadual',
            'institutional_contact': 'Contato Institucional',
            'institutional_email': 'E-mail Institucional',
            'address': 'Endereço Principal',
            'logo': 'Logotipo da Empresa',
            'legal_rep_name': 'Nome Completo do Responsável',
            'legal_rep_role': 'Cargo/Função do Responsável',
            'legal_rep_contact': 'Contato Direto/WhatsApp do Responsável',
            'legal_rep_email': 'Email do Responsável',
        }
