from django.db import models
from Authentication.models import Farmer
from Warehouser.models import Warehouse
from cloudinary.models import CloudinaryField

# Create your models here.
class CoffeeProducts(models.Model):
    name = models.TextField(default="")
    quantity = models.IntegerField(default=0)
    warehouse_approved = models.BooleanField(default=False)
    producer = models.ForeignKey(Farmer,on_delete=models.CASCADE)

class FarmerProfile(models.Model):
    farmer = models.OneToOneField(Farmer,on_delete=models.CASCADE)
    products = models.ManyToManyField(CoffeeProducts)

class WarehousingRequest(models.Model):
    Warehouse =  models.OneToOneField(Warehouse,on_delete=models.SET_NULL)
    farmer = models.OneToOneField(Farmer,on_delete=models.CASCADE)
    products = models.ManyToManyField(CoffeeProducts)
    is_accepted = models.BooleanField(default=False)
    message = models.TextField(default="")

