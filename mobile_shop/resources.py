from import_export import resources
from import_export.fields import Field
from .models import MobileShop, MobileBrand, MobileModel, Inventory

class MobileShopResource(resources.ModelResource):
    class Meta:
        model = MobileShop
        fields = ('id', 'shop_name', 'district', 'address', 'phone', 'is_carrier', 'carrier_name')
        export_order = fields
        import_id_fields = ['id']

class MobileBrandResource(resources.ModelResource):
    class Meta:
        model = MobileBrand
        fields = ('id', 'brand_name', 'country', 'founded_year')
        export_order = fields
        import_id_fields = ['id']

class MobileModelResource(resources.ModelResource):
    brand_name = Field(attribute='brand__brand_name', column_name='品牌名稱')
    
    class Meta:
        model = MobileModel
        fields = ('id', 'model_name', 'brand', 'brand_name', 'price_hkd', 
                  'release_date', 'storage', 'ram')
        export_order = fields
        import_id_fields = ['id']

    def before_import_row(self, row, **kwargs):
        # 如果匯入時提供品牌名稱，自動尋找或建立品牌
        brand_name = row.get('品牌名稱')
        if brand_name:
            brand, _ = MobileBrand.objects.get_or_create(brand_name=brand_name)
            row['brand'] = brand.id

class InventoryResource(resources.ModelResource):
    model_name = Field(attribute='mobile_model__model_name', column_name='型號名稱')
    shop_name = Field(attribute='shop__shop_name', column_name='店舖名稱')
    
    class Meta:
        model = Inventory
        fields = ('id', 'mobile_model', 'model_name', 'shop', 'shop_name', 'quantity')
        export_order = fields
        import_id_fields = ['id']

    def before_import_row(self, row, **kwargs):
        # 匯入時依據型號名稱和店舖名稱查找對應的外鍵
        model_name = row.get('型號名稱')
        shop_name = row.get('店舖名稱')
        if model_name:
            try:
                model = MobileModel.objects.get(model_name=model_name)
                row['mobile_model'] = model.id
            except MobileModel.DoesNotExist:
                raise Exception(f'找不到型號: {model_name}')
        if shop_name:
            try:
                shop = MobileShop.objects.get(shop_name=shop_name)
                row['shop'] = shop.id
            except MobileShop.DoesNotExist:
                raise Exception(f'找不到店舖: {shop_name}')