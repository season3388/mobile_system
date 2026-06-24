import csv
import json
import os
from django.core.management.base import BaseCommand
from mobile_shop.models import MobileShop, MobileBrand, MobileModel, Inventory

class Command(BaseCommand):
    help = '匯出所有資料為 CSV 或 JSON'

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            choices=['csv', 'json'],
            default='csv',
            help='匯出格式 (csv 或 json)'
        )
        parser.add_argument(
            '--file',
            type=str,
            help='輸出檔案名稱（預設為 export_data.格式）',
        )

    def handle(self, *args, **options):
        fmt = options['format']
        filename = options.get('file') or f'export_data.{fmt}'

        data = {
            'MobileShop': list(MobileShop.objects.all().values()),
            'MobileBrand': list(MobileBrand.objects.all().values()),
            'MobileModel': list(MobileModel.objects.all().values()),
            'Inventory': list(Inventory.objects.all().values()),
        }

        if fmt == 'json':
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            self.stdout.write(self.style.SUCCESS(f'已匯出 JSON 至 {filename}'))

        elif fmt == 'csv':
            base = os.path.splitext(filename)[0]
            for model_name, rows in data.items():
                if rows:
                    csv_file = f'{base}_{model_name}.csv'
                    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                        writer.writeheader()
                        writer.writerows(rows)
                    self.stdout.write(f'  - {model_name} 匯出至 {csv_file}')
            self.stdout.write(self.style.SUCCESS(f'所有 CSV 檔案已匯出（前綴：{base}）'))