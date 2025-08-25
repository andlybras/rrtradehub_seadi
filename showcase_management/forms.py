from django import forms
from .models import Product, NCMSubitem

class ProductForm(forms.ModelForm):
    ncm_subitem = forms.ModelChoiceField(
        queryset=NCMSubitem.objects.all(),
        label="NCM (Subitem)",
        widget=forms.HiddenInput() # O usuário selecionará via busca, não por um select padrão
    )

    class Meta:
        model = Product
        fields = ['title', 'description', 'ncm_subitem', 'is_active']
        labels = {
            'title': 'Título do Produto',
            'description': 'Descrição',
            'is_active': 'Manter produto ativo na vitrine',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary'}),
        }
