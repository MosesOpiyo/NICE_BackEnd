from django.db import models
from Authentication.models import Farmer

class CoffeeProducts(models.Model):
    name = models.TextField(default="")
    quantity = models.IntegerField(default=0)
    warehouse_approved = models.BooleanField(default=False)
    producer = models.ForeignKey(Farmer,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class FarmerProfile(models.Model):
    farmer = models.OneToOneField(Farmer,on_delete=models.CASCADE)
    products = models.ManyToManyField(CoffeeProducts)

    def __str__(self):
        return self.farmer.username


