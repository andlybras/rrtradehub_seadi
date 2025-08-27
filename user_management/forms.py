from django import forms
from .models import CustomUser

class BusinessUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

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

class UserChangeRequestForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['razao_social', 'nome_fantasia', 'cnpj', 'email']
        widgets = {
            'razao_social': forms.TextInput(attrs={'class': 'form-input'}),
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-input'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }

class EducationalUserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput(attrs={'class': 'form-input'}) # Adicione attrs aqui
    )
    password2 = forms.CharField(
        label='Confirmação de Senha', 
        widget=forms.PasswordInput(attrs={'class': 'form-input'}) # E aqui também
    )


    class Meta:
        model = CustomUser
        # ADICIONE 'username' A ESTA LISTA
        fields = ('username', 'full_name', 'email', 'date_of_birth', 'education_level')
        widgets = {
            # ADICIONE O WIDGET PARA 'username'
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-input'}
            ),
            'full_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'education_level': forms.Select(attrs={'class': 'form-input'}),
        }

    def clean_password2(self):
        # ... (este método não muda)
        cd = self.cleaned_data
        if cd.get('password') and cd.get('password2') and cd['password'] != cd['password2']:
            raise forms.ValidationError('As senhas não coincidem.')
        return cd.get('password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.user_type = CustomUser.UserType.EDUCATIONAL
        
        # REMOVA O BLOCO DE CÓDIGO QUE GERAVA O USERNAME AUTOMATICAMENTE
        # O username agora virá diretamente do formulário.

        if commit:
            user.save()
        return user