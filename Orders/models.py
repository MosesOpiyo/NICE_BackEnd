from django.db import models
from Authentication.models import Buyer,Farmer,Account
from Farming.models import CoffeeProducts,ProcessedProducts
from Warehouser.models import Warehouse

class CartItem(models.Model):
    product = models.ForeignKey(ProcessedProducts,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0,null=True)
    price = models.IntegerField(default=0)
    grind = models.TextField(default="",null=True)
    roast_type = models.TextField(default="",null=True)
    type = models.TextField(default="")

    def __str__(self):
        return f"Cart Item: {self.id}"

class Cart(models.Model):
    buyer = models.OneToOneField(Account,on_delete=models.CASCADE)
    products = models.ManyToManyField(CartItem)

    def __str__(self):
        return f"{self.buyer}'s Cart"

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
    
