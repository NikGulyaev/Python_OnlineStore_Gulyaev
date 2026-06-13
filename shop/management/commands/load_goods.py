from django.core.management.base import BaseCommand #type: ignore
from django.db import transaction #type: ignore
from shop.models import Product, StockBalance, Category
import csv
from pathlib import Path

class Command(BaseCommand):
    help = 'Загружает товары и остатки из CSV‑файла'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            nargs='?',
            default='goods_data.csv',
            help='Путь к CSV‑файлу с данными (по умолчанию: goods_data.csv)'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        file_path = Path(csv_file)

        if not file_path.exists():
            self.stdout.write(
                self.style.ERROR(f'Файл {csv_file} не найден!')
            )
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                created_count = 0
                updated_count = 0

                with transaction.atomic():
                    for row in reader:
                        # Создаём или получаем категорию
                        category_name = row.get('category', '').strip()
                        if category_name:
                            category, _ = Category.objects.get_or_create(
                            name=category_name,
                            defaults={'description': f'Категория: {category_name}'}
                            )
                        else:
                            category = None

                        # Создаём или обновляем товар
                        product, created = Product.objects.update_or_create(
                        name=row['name'].strip(),
                        defaults={
                        'price': row['price'],
                        'description': row.get('description', ''),
                        'category': category  # передаём экземпляр Category
                            }
                        )

                        # Создаём остаток на складе
                        StockBalance.objects.update_or_create(
                        product=product,
                        defaults={'quantity': int(row['quantity'])}
                        )

                        if created:
                            created_count += 1
                        else:
                            updated_count += 1

            self.stdout.write(
                self.style.SUCCESS(
            f'Успешно загружено: {created_count} новых товаров, '
            f'{updated_count} обновлено'
        )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при загрузке данных: {e}')
            )
