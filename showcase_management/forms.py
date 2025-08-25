from django import forms
from .models import Product, ProductImage, NCMSubitem

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

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True})
        }
