from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

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
    
class OrderItem(models.Model):
    product = models.ForeignKey(ProcessedProducts,on_delete=models.CASCADE,null=True)
    weight = models.CharField(max_length=100,default='',null=True)
    quantity = models.IntegerField(default=0,null=True)
    price = models.FloatField(default=0)
    grind = models.TextField(default="",null=True)
    roast_type = models.TextField(default="",null=True)
    type = models.TextField(default="")
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

class Delivery(models.Model):
    DELIVERY_SPEED_CHOICES = [
        ('standard', 'Standard'),
        ('express', 'Express'),
        ('overnight', 'Overnight'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField(default="",null=True)
    country = models.TextField(default="",null=True)
    state = models.TextField(default="",null=True)
    city = models.TextField(default="",null=True)
    company_name = models.TextField(default="",null=True)
    residence = models.TextField(default="",null=True)
    postal_code = models.TextField(default="",null=True)
    email = models.EmailField(default="",null=True)
    phone_number = models.CharField(max_length=15)
    delivery_speed = models.CharField(max_length=50, choices=DELIVERY_SPEED_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.delivery_speed}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    voucher_number = models.CharField(max_length=50, null=True, blank=True)
    promo_code = models.CharField(max_length=50, null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    card_last_4_digits = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self):
        return f"{self.payment_method} - {self.billing_region}"


class Billing(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField(default="")
    country = models.TextField(default="")
    city = models.TextField(default="")
    state = models.TextField(default="")
    residence = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class ProductOrder(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    order = models.ForeignKey('Order', related_name='product_orders', on_delete=models.CASCADE,null=True)

    def clean(self):
        """Ensure content_type only points to CartItem or OrderItem."""
        allowed_models = [CartItem, OrderItem]
        if self.content_type.model_class() not in allowed_models:
            raise ValidationError(f"Invalid model. Only {allowed_models} are allowed.")

class Order(models.Model):
    buyer = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    total = models.FloatField(default=0)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE,null=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE,null=True)
    billing = models.ForeignKey(Billing, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    is_fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id}"

    
