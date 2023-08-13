from django.db import models
from Authentication.models import Warehouser
from Farmer.models import CoffeeProducts

class Warehouse(models.Model):
    warehouser = models.OneToOneField(Warehouser,on_delete=models.CASCADE)
    warehoused_products = models.ManyToManyField(CoffeeProducts)
    name = models.TextField(default="")
    location = models.TextField(default="")
    
    def __str__(self):
        return self.name
     
