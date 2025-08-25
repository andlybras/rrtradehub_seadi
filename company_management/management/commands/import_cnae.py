import re
import xlrd
from django.core.management.base import BaseCommand, CommandError
from company_management.models import CNAE

class Command(BaseCommand):
    help = 'Importa os códigos CNAE a partir de um arquivo .xls.'

    def add_arguments(self, parser):
        parser.add_argument('xls_file', type=str, help='O caminho para o arquivo .xls.')

    def handle(self, *args, **options):
        file_path = options['xls_file']
        cnae_pattern = re.compile(r'^\d{4}-\d\/\d{2}$')

        try:
            workbook = xlrd.open_workbook(file_path, encoding_override="latin-1")
            sheet = workbook.sheet_by_index(0)
        except Exception as e:
            raise CommandError(f'Falha ao abrir o arquivo Excel: {e}')

        header_row_index = -1
        subclasse_col_index = -1
        denominacao_col_index = -1

        for i in range(sheet.nrows):
            row_values = [str(cell.value).strip() for cell in sheet.row(i)]
            if 'Subclasse' in row_values and 'Denominação' in row_values:
                header_row_index = i
                subclasse_col_index = row_values.index('Subclasse')
                denominacao_col_index = row_values.index('Denominação')
                break
        
        if header_row_index == -1:
            # Fallback for the second header format found in diagnostics
            for i in range(sheet.nrows):
                row_values = [str(cell.value).strip() for cell in sheet.row(i)]
                if 'Seção' in row_values and 'Subclasse' in row_values:
                    header_row_index = i
                    subclasse_col_index = row_values.index('Subclasse')
                    # The 'Denominação' is in the next column in this format
                    if len(row_values) > subclasse_col_index + 1:
                         denominacao_col_index = subclasse_col_index + 1
                    break

        if header_row_index == -1 or subclasse_col_index == -1 or denominacao_col_index == -1:
            raise CommandError("Não foi possível encontrar as colunas de cabeçalho 'Subclasse' e 'Denominação' no arquivo.")

        created_count = 0
        skipped_count = 0
        self.stdout.write(self.style.SUCCESS('Iniciando a importação dos códigos CNAE...'))

        for i in range(header_row_index + 1, sheet.nrows):
            if sheet.ncols > max(subclasse_col_index, denominacao_col_index):
                cnae_code = str(sheet.cell_value(i, subclasse_col_index)).strip()
                cnae_description = str(sheet.cell_value(i, denominacao_col_index)).strip()

                if cnae_pattern.match(cnae_code) and cnae_description:
                    obj, created = CNAE.objects.get_or_create(
                        code=cnae_code,
                        defaults={'description': cnae_description}
                    )
                    if created:
                        created_count += 1
                    else:
                        skipped_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'\nImportação finalizada!'))
        self.stdout.write(self.style.SUCCESS(f'{created_count} novos códigos CNAE foram criados.'))
        self.stdout.write(self.style.WARNING(f'{skipped_count} códigos já existiam e foram ignorados.'))
