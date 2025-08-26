from django import forms
from .models import Chart
import demjson3

class ChartAdminForm(forms.ModelForm):
    options_js_input = forms.CharField(
        label="Opções de Configuração (Código do Exemplo ECharts)",
        widget=forms.Textarea(attrs={'rows': 20, 'cols': 80}),
        help_text="Cole o objeto 'option' completo do exemplo do ECharts aqui. A conversão para JSON será feita automaticamente."
    )

    class Meta:
        model = Chart
        fields = ('name', 'slug', 'options_json')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.options_json:
            try:
                self.fields['options_js_input'].initial = demjson3.encode(self.instance.options_json, compactly=False)
            except:
                self.fields['options_js_input'].initial = self.instance.options_json

    def clean(self):
        cleaned_data = super().clean()
        js_code = cleaned_data.get('options_js_input')

        if js_code:
            try:
                if js_code.strip().startswith('option ='):
                    js_code = js_code.split('option =', 1)[1]

                decoded_json = demjson3.decode(js_code)
                cleaned_data['options_json'] = decoded_json
            except demjson3.DecodeError as e:
                raise forms.ValidationError(f"Erro de sintaxe no código do gráfico. Verifique o código perto de: {e}")

        return cleaned_data