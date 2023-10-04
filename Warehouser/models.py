from django.db import models
from Authentication.models import Warehouser,Buyer
from Farming.models import CoffeeProducts,ProcessedProducts
    
class Warehouse(models.Model):
    warehouser = models.OneToOneField(Warehouser,on_delete=models.CASCADE)
    warehoused_products = models.ManyToManyField(CoffeeProducts)
    processed_products = models.ManyToManyField(ProcessedProducts)
    name = models.TextField(default="")
    location = models.TextField(default="")
    
    def __str__(self):
        return self.name
    
class ShippingManifest(models.Model):
    number = models.CharField(max_length=10,default="")
    warehouser = models.ForeignKey(Warehouser,on_delete=models.CASCADE)
    product = models.OneToOneField(CoffeeProducts,on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    shipping_approval = models.BooleanField(default=False)
    
    def __str__(self):
        return str(f"{self.number} - {self.product.name}")
     
