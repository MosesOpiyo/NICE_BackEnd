from django.db import models
from Orders.models import Order
from Authentication.models import Account
from Orders.models import CartItem,Cart

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
    order = models.OneToOneField(Order,on_delete=models.CASCADE,null=True)
    payment_id = models.CharField(max_length=35,default="")

class Subscription(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItem,related_name="subscriptions")
    amount = models.FloatField(default=0)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.user} - {self.start_date}"
    
    def new_Subscription(request):
        user = Account.objects.get(id=request.user.id)
        cart = Cart.objects.get(buyer=user)
        cart_items = cart.products.filter(subscription=True)
        amount = sum(item.price for item in cart_items)
        subscription = Subscription.objects.create(
            user = user,
            amount = amount 
        )
        subscription.cart_items.set(cart_items)
        subscription.save()
        return subscription