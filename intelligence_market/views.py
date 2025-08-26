from django.shortcuts import render, get_object_or_404
from .models import AnalysisPage, Chart
import re
# O import de 'json' não é mais necessário para esta view, mas podemos manter por via das dúvidas.
import json

# View para a página principal, que lista todos os cards
def indicator_list_view(request):
    # Buscamos apenas as páginas que estão marcadas como "Publicado"
    pages = AnalysisPage.objects.filter(is_published=True)
    context = {
        'pages': pages
    }
    return render(request, 'intelligence_market/indicator_list.html', context)

# View para a página de detalhe, que mostra o gráfico e o texto
def indicator_detail_view(request, pk):
    page = get_object_or_404(AnalysisPage, pk=pk, is_published=True)
    
    # --- A MÁGICA ATUALIZADA ACONTECE AQUI ---
    # Esta função será usada para substituir cada shortcode encontrado
    def replace_shortcode(match):
        slug = match.group(1)
        try:
            chart = Chart.objects.get(slug=slug)
            
            # A string de retorno é onde faremos a mudança
            return f"""
            <div id="chart-{chart.slug}" style="width: 100%; height: 400px;" class="my-6"></div>
            <script type="text/javascript">
                var chartDom = document.getElementById('chart-{chart.slug}');
                var myChart = echarts.init(chartDom);
                var option; // Declaramos a variável option aqui
                
                // --- MUDANÇA PRINCIPAL AQUI ---
                // Simplesmente executamos o bloco de código do admin.
                // Ele é responsável por definir o valor da variável 'option'.
                {chart.options_js} 
                
                myChart.setOption(option);
            </script>
            """
        except Chart.DoesNotExist:
            return f'<p class="text-red-500">Erro: Gráfico com slug "{slug}" não encontrado.</p>'

    processed_content = re.sub(r'\[chart:(.*?)\]', replace_shortcode, page.content)

    context = {
        'page': page,
        'processed_content': processed_content,
    }
    return render(request, 'intelligence_market/indicator_detail.html', context)