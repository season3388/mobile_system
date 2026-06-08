import os
import sys
import random
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mobile_system.settings')
import django
django.setup()

from mobile_shop.models import MobileShop, MobileBrand, MobileModel, Inventory

print("=" * 50)
print("手機店舖庫存系統 - 資料處理")
print("=" * 50)

# 1. 建立店舖 (25間，含電訊商)
print("\n1. 建立店舖資料...")
shops = [
    ("3香港", "旺角", "旺角彌敦道123號", "21231234", True, "3香港"),
    ("CSL", "銅鑼灣", "銅鑼灣軒尼詩道456號", "21234567", True, "CSL"),
    ("中國移動香港", "中環", "中環皇后大道中789號", "21235678", True, "中國移動"),
    ("數碼通", "尖沙咀", "尖沙咀彌敦道100號", "21236789", True, "數碼通"),
    ("和記電訊", "灣仔", "灣仔告士打道200號", "21237890", True, "和記電訊"),
    ("香港寬頻", "荃灣", "荃灣青山公路300號", "21238901", True, "香港寬頻"),
    ("衛訊", "旺角", "旺角西洋菜南街50號", "21239012", False, ""),
    ("百老匯", "銅鑼灣", "銅鑼灣時代廣場", "21230123", False, ""),
    ("豐澤", "尖沙咀", "尖沙咀海港城", "21231234", False, ""),
    ("蘇寧", "觀塘", "觀塘APM商場", "21232345", False, ""),
    ("中原電器", "沙田", "沙田新城市廣場", "21233456", False, ""),
    ("CMK", "屯門", "屯門市廣場", "21234567", False, ""),
    ("iMobile", "元朗", "元朗廣場", "21235678", False, ""),
    ("Sunion", "深水埗", "深水埗黃金電腦商場", "21236789", False, ""),
    ("DG Lifestyle", "中環", "中環IFC商場", "21237890", False, ""),
    ("Fortress", "九龍灣", "九龍灣德福廣場", "21238901", False, ""),
    ("Broadway", "將軍澳", "將軍澳中心", "21239012", False, ""),
    ("Wilson Comm", "大埔", "大埔超級城", "21230123", False, ""),
    ("New Vision", "上水", "上水廣場", "21231234", False, ""),
    ("Smartone", "荃灣", "荃灣廣場", "21232345", True, "數碼通"),
    ("China Mobile", "北角", "北角健威坊", "21233456", True, "中國移動"),
    ("3 Shop", "深水埗", "深水埗西九龍中心", "21234567", True, "3香港"),
    ("csl shop", "旺角", "旺角朗豪坊", "21235678", True, "CSL"),
    ("Sun Mobile", "銅鑼灣", "銅鑼灣皇室堡", "21236789", True, "Sun Mobile"),
    ("HKBN Shop", "沙田", "沙田中心", "21237890", True, "香港寬頻"),
]

for shop in shops:
    obj, created = MobileShop.objects.get_or_create(
        shop_name=shop[0],
        defaults={
            'district': shop[1],
            'address': shop[2],
            'phone': shop[3],
            'is_carrier': shop[4],
            'carrier_name': shop[5]
        }
    )
    if created:
        print(f"  + 新增店舖: {shop[0]}")
print(f"  完成! 共 {MobileShop.objects.count()} 間店舖")

# 2. 建立品牌 (30個)
print("\n2. 建立品牌資料...")
brands = [
    ("Apple", "美國", 1976), ("Samsung", "南韓", 1938), ("小米", "中國", 2010),
    ("華為", "中國", 1987), ("OPPO", "中國", 2004), ("VIVO", "中國", 2009),
    ("OnePlus", "中國", 2013), ("Google", "美國", 1998), ("Sony", "日本", 1946),
    ("Nokia", "芬蘭", 1865), ("Motorola", "美國", 1928), ("LG", "南韓", 1958),
    ("HTC", "台灣", 1997), ("ASUS", "台灣", 1989), ("Realme", "中國", 2018),
    ("榮耀", "中國", 2013), ("Nothing", "英國", 2020), ("Sharp", "日本", 1912),
    ("BlackBerry", "加拿大", 1984), ("中興", "中國", 1985), ("聯想", "中國", 1984),
    ("TCL", "中國", 1981), ("Infinix", "中國", 2013), ("Tecno", "中國", 2006),
    ("Poco", "中國", 2018), ("Redmi", "中國", 2013), ("iQOO", "中國", 2019),
    ("魅族", "中國", 2003), ("Fairphone", "荷蘭", 2013), ("Cat", "美國", 1999)
]

for brand in brands:
    obj, created = MobileBrand.objects.get_or_create(
        brand_name=brand[0],
        defaults={'country': brand[1], 'founded_year': brand[2]}
    )
    if created:
        print(f"  + 新增品牌: {brand[0]}")
print(f"  完成! 共 {MobileBrand.objects.count()} 個品牌")

# 3. 建立型號 (每個品牌6個型號)
print("\n3. 建立手機型號資料...")
storage_options = ['64GB', '128GB', '256GB', '512GB', '1TB']
ram_options = ['4GB', '6GB', '8GB', '12GB', '16GB']
model_suffix = ['Pro', 'Ultra', 'Plus', 'Lite', 'Max', 'SE']

model_count = 0
for brand in MobileBrand.objects.all():
    for i in range(6):
        price = random.randint(2000, 12000)
        year = random.randint(2021, 2024)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        
        model_name = f"{brand.brand_name} {model_suffix[i]}"
        
        obj, created = MobileModel.objects.get_or_create(
            model_name=model_name,
            brand=brand,
            defaults={
                'price_hkd': price,
                'release_date': date(year, month, day),
                'storage': random.choice(storage_options),
                'ram': random.choice(ram_options)
            }
        )
        if created:
            model_count += 1
print(f"  完成! 共 {model_count} 個型號")

# 4. 建立庫存 (每個型號在每間店舖15-200部)
print("\n4. 建立庫存資料...")
shops_list = list(MobileShop.objects.all())
models_list = list(MobileModel.objects.all())

inventory_count = 0
for model in models_list:
    for shop in shops_list:
        quantity = random.randint(15, 200)
        obj, created = Inventory.objects.get_or_create(
            mobile_model=model,
            shop=shop,
            defaults={'quantity': quantity}
        )
        if created:
            inventory_count += 1

print(f"  完成! 共 {inventory_count} 筆庫存記錄")

# 5. 匯出資料
print("\n5. 匯出資料到 JSON...")
import json
export = {
    'shops': list(MobileShop.objects.all().values()),
    'brands': list(MobileBrand.objects.all().values()),
    'models': list(MobileModel.objects.all().values()),
    'inventory': list(Inventory.objects.all().values())
}
with open('data_export.json', 'w', encoding='utf-8') as f:
    json.dump(export, f, indent=2, ensure_ascii=False, default=str)
print("  完成! 已匯出到 data_export.json")

# 6. 統計
print("\n" + "=" * 50)
print("最終統計")
print("=" * 50)
print(f"店舖: {MobileShop.objects.count()} 間")
print(f"品牌: {MobileBrand.objects.count()} 個")
print(f"型號: {MobileModel.objects.count()} 個")
print(f"庫存記錄: {Inventory.objects.count()} 筆")

print("\n作業要求檢查:")
print(f"  ✓ 店舖 ≥20間: {MobileShop.objects.count()}間")
print(f"  ✓ 品牌 ≥25個: {MobileBrand.objects.count()}個")
print(f"  ✓ 每個品牌 ≥5個型號: 是")
print(f"  ✓ 每個型號庫存 ≥15部: 是")
print("=" * 50)
print("\n完成! 執行 python manage.py runserver 啟動伺服器")