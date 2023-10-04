from django.db import models
from Authentication.models import Buyer,Farmer
from Farming.models import CoffeeProducts,ProcessedProducts
from Warehouser.models import Warehouse

class Cart(models.Model):
    buyer = models.OneToOneField(Buyer,on_delete=models.CASCADE)
    products = models.ManyToManyField(CoffeeProducts)

class Order(models.Model):
    buyer = models.OneToOneField(Buyer,on_delete=models.CASCADE)
    product = models.OneToOneField(CoffeeProducts,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    warehouse = models.OneToOneField(Warehouse,on_delete=models.CASCADE,null=True)
    country = models.TextField(default="")
    date = models.DateField(null=True,blank=True)
    marker = models.IntegerField(default=0)
    is_fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    
