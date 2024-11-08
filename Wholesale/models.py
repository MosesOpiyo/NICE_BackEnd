from django.db import models

from Authentication.models import Account

# Create your models here.
class WholesaleEnterprise(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE)
    full_names = models.TextField(default="")
    business_name = models.TextField(default="")
    email = models.CharField(max_length=100,default="")
    phone_number = models.TextField(default="")
    type_of_business = models.TextField(default="")
    shipping_address = models.TextField(default="")
    business_status = models.TextField(default="")
    duration_of_operation = models.CharField(max_length=200)
    date_to_start_operating = models.DateField(null=True,blank=True)
    quantity = models.TextField(default="",null=True)
    need_equipemnt = models.BooleanField(default=False)
    date_to_start_receiving_coffee_orders = models.DateField(null=True,blank=True)
    more_about_the_business = models.TextField(default="")

    def str_to_bool(s):
        return s.lower() in ['true', '1', 'yes', 'y']