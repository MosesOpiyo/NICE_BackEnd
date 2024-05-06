from django.db import models
from Orders.models import Order
from Authentication.models import Account

import datetime

# Create your models here.
class Payments(models.Model):
    order = models.OneToOneField(Order,on_delete=models.CASCADE,null=True)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f"Payment: {self.id}"
    
class Address(models.Model):
    email = models.TextField(default="")
    first_name = models.TextField(default="")
    last_name = models.TextField(default="")
    phone_number = models.TextField(default="")
    address = models.TextField(default="")
    company_address = models.TextField(default="",null=True)
    country = models.TextField(default="")
    region = models.TextField(default="")
    city = models.TextField(default="")
    place_of_residence = models.TextField(default="",null=True)
    postal_code = models.TextField(default="") 

class Receipt(models.Model):
    address_info = models.OneToOneField(Address,on_delete=models.CASCADE,null=True)
    amount = models.FloatField(default=0)
    buyer = models.ForeignKey(Account, on_delete=models.CASCADE,null=True)
    payment_option = models.TextField(default="")
    shipping_option = models.TextField(default="")
    creation_date = models.DateTimeField()
    paid = models.BooleanField(default=False)