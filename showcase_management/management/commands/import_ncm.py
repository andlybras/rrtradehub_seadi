import json
import re
from django.core.management.base import BaseCommand, CommandError
from showcase_management.models import NCMChapter, NCMPosition, NCMSubitem
from django.db import transaction

class Command(BaseCommand):
    help = 'Importa os códigos NCM a partir de um arquivo JSON.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='O caminho para o arquivo NCM JSON.')

    def handle(self, *args, **options):
        file_path = options['json_file']

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            raise CommandError(f'Arquivo "{file_path}" não encontrado.')
        except json.JSONDecodeError:
            raise CommandError('Erro ao decodificar o arquivo JSON. Verifique o formato.')

        nomenclaturas = data.get('Nomenclaturas', [])
        if not nomenclaturas:
            raise CommandError('Nenhuma nomenclatura encontrada no arquivo JSON.')

        # Usamos uma transação para garantir que todos os dados sejam importados ou nenhum.
        try:
            with transaction.atomic():
                self.stdout.write(self.style.SUCCESS('Iniciando a importação dos códigos NCM...'))
                
                chapters = {}
                positions = {}

                # Primeira passagem para criar Capítulos e Posições
                for item in nomenclaturas:
                    code = item.get('Codigo', '').replace('.', '')
                    description = item.get('Descricao', '')

                    # Limpa tags HTML da descrição
                    description = re.sub('<[^<]+?>', '', description)

                    if len(code) == 2:
                        chapter, created = NCMChapter.objects.get_or_create(
                            code=code,
                            defaults={'description': description}
                        )
                        chapters[code] = chapter
                        if created:
                            self.stdout.write(f'  Capítulo criado: {chapter}')

                    elif len(code) == 4:
                        chapter_code = code[:2]
                        chapter_obj = chapters.get(chapter_code)
                        if chapter_obj:
                            position, created = NCMPosition.objects.get_or_create(
                                code=code,
                                defaults={'chapter': chapter_obj, 'description': description}
                            )
                            positions[code] = position
                            if created:
                                self.stdout.write(f'    Posição criada: {position}')

                # Segunda passagem para criar Subitens
                for item in nomenclaturas:
                    code = item.get('Codigo', '').replace('.', '')
                    description = item.get('Descricao', '')
                    description = re.sub('<[^<]+?>', '', description)

                    if len(code) == 8:
                        position_code = code[:4]
                        position_obj = positions.get(position_code)
                        if position_obj:
                            subitem, created = NCMSubitem.objects.get_or_create(
                                code=code,
                                defaults={'position': position_obj, 'description': description}
                            )
                            if created:
                                self.stdout.write(f'      Subitem criado: {subitem}')

        except Exception as e:
            raise CommandError(f'Ocorreu um erro durante a importação: {e}')

        self.stdout.write(self.style.SUCCESS('Importação do NCM concluída com sucesso!'))

