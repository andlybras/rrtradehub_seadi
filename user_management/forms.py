from django import forms
from .models import CustomUser

class BusinessUserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput,
        help_text="Sua senha não pode ser muito parecida com suas outras informações pessoais."
    )
    password2 = forms.CharField(
        label='Confirmação de Senha', 
        widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'razao_social', 'nome_fantasia', 'cnpj')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') and cd.get('password2') and cd['password'] != cd['password2']:
            raise forms.ValidationError('As senhas não coincidem.')
        return cd.get('password2')
    
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if CustomUser.objects.filter(cnpj=cnpj).exists():
            raise forms.ValidationError("Um usuário com este CNPJ já existe.")
        return cnpj

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.user_type = CustomUser.UserType.BUSINESS
        if commit:
            user.save()
        return user
