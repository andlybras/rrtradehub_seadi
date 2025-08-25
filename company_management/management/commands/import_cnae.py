import csv
from django.core.management.base import BaseCommand, CommandError
from company_management.models import CNAE
import re

class Command(BaseCommand):
    help = 'Importa os códigos CNAE a partir de um arquivo CSV fornecido.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='O caminho para o arquivo CSV a ser importado.')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        cnae_pattern = re.compile(r'^\d{4}-\d\/\d{2}$')

        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                
                created_count = 0
                skipped_count = 0

                self.stdout.write(self.style.SUCCESS('Iniciando a importação dos códigos CNAE...'))

                for row in reader:
                    if len(row) > 5:
                        cnae_code = row[5].strip()
                        cnae_description = row[6].strip() if len(row) > 6 else ''
                        
                        if cnae_pattern.match(cnae_code):
                            obj, created = CNAE.objects.get_or_create(
                                code=cnae_code,
                                defaults={'description': cnae_description}
                            )
                            
                            if created:
                                created_count += 1
                                self.stdout.write(f'CNAE criado: {cnae_code} - {cnae_description}')
                            else:
                                skipped_count += 1

                self.stdout.write(self.style.SUCCESS(f'\nImportação concluída!'))
                self.stdout.write(self.style.SUCCESS(f'{created_count} novos códigos CNAE foram criados.'))
                self.stdout.write(self.style.WARNING(f'{skipped_count} códigos já existiam e foram ignorados.'))

        except FileNotFoundError:
            raise CommandError(f'Arquivo não encontrado em: "{csv_file_path}"')
        except Exception as e:
            raise CommandError(f'Ocorreu um erro ao processar o arquivo: {e}')