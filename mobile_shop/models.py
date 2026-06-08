from django.db import models

class MobileShop(models.Model):
    shop_name = models.CharField(max_length=100, verbose_name='店舖名稱')
    district = models.CharField(max_length=50, verbose_name='地區')
    address = models.TextField(verbose_name='地址')
    phone = models.CharField(max_length=20, verbose_name='聯絡電話')
    is_carrier = models.BooleanField(default=False, verbose_name='是否為電訊網絡供應商')
    carrier_name = models.CharField(max_length=100, blank=True, verbose_name='供應商名稱')
    
    class Meta:
        verbose_name = '手機店舖'
        verbose_name_plural = '手機店舖'
    
    def __str__(self):
        return self.shop_name


class MobileBrand(models.Model):
    brand_name = models.CharField(max_length=100, unique=True, verbose_name='品牌名稱')
    country = models.CharField(max_length=50, verbose_name='來源國家')
    founded_year = models.IntegerField(null=True, blank=True, verbose_name='成立年份')
    
    class Meta:
        verbose_name = '手機品牌'
        verbose_name_plural = '手機品牌'
    
    def __str__(self):
        return self.brand_name


class MobileModel(models.Model):
    model_name = models.CharField(max_length=100, verbose_name='型號名稱')
    brand = models.ForeignKey(MobileBrand, on_delete=models.CASCADE, related_name='models')
    price_hkd = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='港幣零售價')
    release_date = models.DateField(verbose_name='發佈日期')
    storage = models.CharField(max_length=20, verbose_name='儲存容量')
    ram = models.CharField(max_length=10, verbose_name='記憶體')
    
    class Meta:
        verbose_name = '手機型號'
        verbose_name_plural = '手機型號'
    
    def __str__(self):
        return f"{self.brand.brand_name} {self.model_name}"


class Inventory(models.Model):
    mobile_model = models.ForeignKey(MobileModel, on_delete=models.CASCADE, related_name='inventories')
    shop = models.ForeignKey(MobileShop, on_delete=models.CASCADE, related_name='inventories')
    quantity = models.IntegerField(default=0, verbose_name='庫存數量')
    
    class Meta:
        verbose_name = '庫存記錄'
        verbose_name_plural = '庫存記錄'
    
    def __str__(self):
        return f"{self.mobile_model} @ {self.shop}: {self.quantity}部"