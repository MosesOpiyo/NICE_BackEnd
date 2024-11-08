from django.db import models
from Authentication.models import Buyer,Farmer,Account
from Farming.models import CoffeeProducts,ProcessedProducts
from Warehouser.models import Warehouse

class CartItem(models.Model):
    product = models.ForeignKey(ProcessedProducts,on_delete=models.CASCADE)
    weight = models.CharField(max_length=100,default='',null=True)
    quantity = models.IntegerField(default=0,null=True)
    price = models.FloatField(default=0)
    grind = models.TextField(default="",null=True)
    roast_type = models.TextField(default="",null=True)
    type = models.TextField(default="")
    subscription = models.BooleanField(default=False)
    frequency = models.TextField(default="")
    code = models.CharField(max_length=10,default="") 
    def __str__(self):
        return f"Cart Item: {self.id}"

class Sample(models.Model):
    product = models.ForeignKey(ProcessedProducts,on_delete=models.CASCADE)
    weight = models.CharField(max_length=100,default='',null=True)
    quantity = models.IntegerField(default=0,null=True)
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.product} Sample"

class Cart(models.Model):
    buyer = models.OneToOneField(Account,on_delete=models.CASCADE,null=True)
    products = models.ManyToManyField(CartItem)
    samples = models.ManyToManyField(Sample)
    wishlist = models.ManyToManyField(ProcessedProducts)
    session_id = models.CharField(max_length = 100,default="",unique=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.buyer}'s Cart"
    
    def delete_unclaimed_carts():
        carts = Cart.objects.filter(buyer__isnull=True)
        carts.delete()


class Order(models.Model):
    buyer = models.ForeignKey(Account,on_delete=models.CASCADE)
    product = models.ManyToManyField(CartItem)
    quantity = models.IntegerField(default=0)
    warehouse = models.ForeignKey(Warehouse,on_delete=models.CASCADE,null=True)
    country = models.TextField(default="")
    date = models.DateTimeField(null=True,blank=True,auto_now=True)
    marker = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    is_fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    
