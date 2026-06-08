from django.contrib import admin
from .models import MobileShop, MobileBrand, MobileModel, Inventory

@admin.register(MobileShop)
class MobileShopAdmin(admin.ModelAdmin):
    list_display = ['shop_name', 'district', 'is_carrier', 'carrier_name', 'phone']
    search_fields = ['shop_name', 'district']

@admin.register(MobileBrand)
class MobileBrandAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'country', 'founded_year']
    search_fields = ['brand_name']

@admin.register(MobileModel)
class MobileModelAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'brand', 'price_hkd', 'storage', 'ram']
    search_fields = ['model_name', 'brand__brand_name']

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['mobile_model', 'shop', 'quantity']
    search_fields = ['mobile_model__model_name', 'shop__shop_name']