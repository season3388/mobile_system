import csv
import json
import os
from django.core.management.base import BaseCommand
from mobile_shop.models import MobileShop, MobileBrand, MobileModel, Inventory

class Command(BaseCommand):
    help = '從 CSV 或 JSON 檔案匯入資料'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            required=True,
            help='要匯入的檔案名稱（支援 CSV 或 JSON）'
        )
        parser.add_argument(
            '--model',
            type=str,
            choices=['MobileShop', 'MobileBrand', 'MobileModel', 'Inventory'],
            help='指定要匯入的模型（僅 CSV 時需要）'
        )

    def handle(self, *args, **options):
        filename = options['file']
        model_name = options.get('model')

        if not os.path.exists(filename):
            self.stderr.write(self.style.ERROR(f'檔案 {filename} 不存在'))
            return

        ext = os.path.splitext(filename)[1].lower()
        if ext == '.json':
            self._import_json(filename)
        elif ext == '.csv':
            if not model_name:
                self.stderr.write(self.style.ERROR('CSV 匯入必須指定 --model 參數'))
                return
            self._import_csv(filename, model_name)
        else:
            self.stderr.write(self.style.ERROR('不支援的檔案格式，請使用 .csv 或 .json'))

    def _import_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        model_map = {
            'MobileShop': MobileShop,
            'MobileBrand': MobileBrand,
            'MobileModel': MobileModel,
            'Inventory': Inventory,
        }
        for model_key, rows in data.items():
            if model_key not in model_map:
                continue
            model = model_map[model_key]
            count = 0
            for row in rows:
                try:
                    obj_id = row.get('id')
                    if obj_id:
                        instance = model.objects.filter(id=obj_id).first()
                        if instance:
                            for k, v in row.items():
                                setattr(instance, k, v)
                            instance.save()
                        else:
                            model.objects.create(**row)
                    else:
                        model.objects.create(**row)
                    count += 1
                except Exception as e:
                    self.stderr.write(self.style.WARNING(f'跳過 {model_key} 記錄 {row}: {e}'))
            self.stdout.write(self.style.SUCCESS(f'匯入 {model_key}: {count} 筆'))

    def _import_csv(self, filename, model_name):
        model_map = {
            'MobileShop': MobileShop,
            'MobileBrand': MobileBrand,
            'MobileModel': MobileModel,
            'Inventory': Inventory,
        }
        model = model_map.get(model_name)
        if not model:
            self.stderr.write(self.style.ERROR(f'未知模型: {model_name}'))
            return

        with open(filename, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        count = 0
        for row in rows:
            try:
                for key, value in row.items():
                    if key in ['id', 'founded_year', 'quantity']:
                        if value:
                            row[key] = int(value)
                    elif key in ['price_hkd']:
                        if value:
                            row[key] = float(value)
                    elif key in ['is_carrier']:
                        row[key] = value.lower() in ['true', '1', 'yes']
                # 簡化外鍵處理，僅示範
                obj_id = row.get('id')
                if obj_id:
                    instance = model.objects.filter(id=obj_id).first()
                    if instance:
                        for k, v in row.items():
                            if k != 'id':
                                setattr(instance, k, v)
                        instance.save()
                    else:
                        model.objects.create(**row)
                else:
                    model.objects.create(**row)
                count += 1
            except Exception as e:
                self.stderr.write(self.style.WARNING(f'跳過記錄 {row}: {e}'))
        self.stdout.write(self.style.SUCCESS(f'匯入完成，共 {count} 筆'))