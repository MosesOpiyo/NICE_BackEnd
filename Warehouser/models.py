from django.db import models
from Authentication.models import Account
from Farming.models import CoffeeProducts,ProcessedProducts

class ShippingManifest(models.Model):
    number = models.BigIntegerField(null=True)
    warehouser = models.TextField(default="")
    product = models.ForeignKey(CoffeeProducts,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=0)
    created = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    shipping_approval = models.BooleanField(default=False)
    
    def __str__(self):
        return str(f"{self.number} - {self.product.name}")

class Pocket(models.Model):
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(CoffeeProducts,on_delete=models.CASCADE) 

class Warehouse(models.Model):
    warehouser = models.OneToOneField(Account,on_delete=models.CASCADE)
    warehoused_products = models.ManyToManyField(ShippingManifest)
    processed_products = models.ManyToManyField(ProcessedProducts)
    name = models.TextField(default="")
    location = models.TextField(default="")
    warehouse_area_storage = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    

   
