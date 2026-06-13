from django.core.management.base import BaseCommand
from shop.models import StockBalance
import json
import csv
from pathlib import Path
from datetime import datetime

class Command(BaseCommand):
    help = 'Экспортирует данные об остатках товаров в JSON или CSV'

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            type=str,
            choices=['json', 'csv'],
            default='json',
            help='Формат экспорта: json или csv (по умолчанию: json)'
        )
        parser.add_argument(
            '--output',
            type=str,
            default='product_residues.json',
            help='Имя выходного файла (по умолчанию: product_residues.json)'
        )

    def handle(self, *args, **options):
        format_type = options['format']
        output_file = options['output']

        # Получаем все остатки товаров
        stock_balances = StockBalance.objects.select_related('product').all()

        if not stock_balances.exists():
            self.stdout.write(
                self.style.WARNING('Нет данных об остатках товаров для экспорта!')
            )
            return

        # Подготавливаем данные
        data = []
        for balance in stock_balances:
            data.append({
                'product_id': balance.product.id,
                'product_name': balance.product.name,
                'category': balance.product.category.name if balance.product.category else 'Без категории',
                'price': str(balance.product.price),
                'quantity': balance.quantity,
                'updated_at': balance.updated_at.isoformat()
            })

        # Экспорт в JSON
        if format_type == 'json':
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.stdout.write(
                self.style.SUCCESS(f'Данные успешно экспортированы в JSON: {output_file}')
            )

        # Экспорт в CSV
        elif format_type == 'csv':
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['product_id', 'product_name', 'category', 'price', 'quantity', 'updated_at']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            self.stdout.write(
                self.style.SUCCESS(f'Данные успешно экспортированы в CSV: {output_file}')
            )
