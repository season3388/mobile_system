from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import MobileShop, MobileBrand, MobileModel, Inventory
from .resources import (
    MobileShopResource, MobileBrandResource,
    MobileModelResource, InventoryResource
)

@admin.register(MobileShop)
class MobileShopAdmin(ImportExportModelAdmin):
    resource_class = MobileShopResource
    list_display = ('shop_name', 'district', 'phone', 'is_carrier', 'carrier_name')
    search_fields = ('shop_name', 'district', 'carrier_name')
    list_filter = ('is_carrier', 'district')

@admin.register(MobileBrand)
class MobileBrandAdmin(ImportExportModelAdmin):
    resource_class = MobileBrandResource
    list_display = ('brand_name', 'country', 'founded_year')
    search_fields = ('brand_name', 'country')

@admin.register(MobileModel)
class MobileModelAdmin(ImportExportModelAdmin):
    resource_class = MobileModelResource
    list_display = ('model_name', 'brand', 'price_hkd', 'storage', 'ram', 'release_date')
    search_fields = ('model_name', 'brand__brand_name')
    list_filter = ('brand', 'storage', 'ram')

@admin.register(Inventory)
class InventoryAdmin(ImportExportModelAdmin):
    resource_class = InventoryResource
    list_display = ('mobile_model', 'shop', 'quantity')
    search_fields = ('mobile_model__model_name', 'shop__shop_name')
    list_filter = ('shop__district',)