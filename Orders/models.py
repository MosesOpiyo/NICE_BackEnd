from django.db import models
from Authentication.models import Buyer
from Farming.models import CoffeeProducts

class Cart(models.Model):
    buyer = models.OneToOneField(Buyer,on_delete=models.CASCADE)
    products = models.ManyToManyField(CoffeeProducts)

class Order(models.Model):
    buyer = models.OneToOneField(Buyer,on_delete=models.CASCADE)
    product = models.OneToOneField(CoffeeProducts,on_delete=models.CASCADE)
    is_fulfilled = models.BooleanField(default=False)
