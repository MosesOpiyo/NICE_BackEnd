from django.db import models
from Authentication.models import Warehouser
from Farming.models import CoffeeProducts,Farmer

class Warehouse(models.Model):
    warehouser = models.OneToOneField(Warehouser,on_delete=models.CASCADE)
    warehoused_products = models.ManyToManyField(CoffeeProducts)
    name = models.TextField(default="")
    location = models.TextField(default="")
    
    def __str__(self):
        return self.name
    
class WarehousingRequest(models.Model):
    Warehouse =  models.OneToOneField(Warehouse,on_delete=models.CASCADE)
    farmer = models.OneToOneField(Farmer,on_delete=models.CASCADE)
    products = models.ManyToManyField(CoffeeProducts)
    is_accepted = models.BooleanField(default=False)
    message = models.TextField(default="")

    def __str__(self):
        return self.Warehouse.name
     
