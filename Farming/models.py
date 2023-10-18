from django.db import models
from cloudinary.models import CloudinaryField
from Authentication.models import Account,Farmer,Buyer
from decouple import config

class CoffeeProducts(models.Model):
    name = models.TextField(default="")
    quantity = models.IntegerField(default=0)
    warehouse_approved = models.BooleanField(default=False)
    producer = models.ForeignKey(Account,on_delete=models.CASCADE,default="")
    email = models.TextField(default="")
    grade = models.CharField(max_length=3,default="")
    origin = models.TextField(default="")
    lot_type = models.TextField(default="")
    cup_score = models.IntegerField(default=0)
    cup_notes = models.TextField(default="")
    cupped_by = models.TextField(default="")
    processing = models.TextField(default="")
    drying = models.TextField(default="")
    caffeine = models.TextField(default="")
    acidity = models.TextField(default="")
    date = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField(default=0)
    requested_warehousing = models.BooleanField(default=False)
    shipment_successful = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Ratings(models.Model):
    user=models.OneToOneField(Buyer,on_delete=models.CASCADE)
    rating=models.IntegerField(default=0)
    comment=models.TextField(default="")

    def __str__(self):
        return f"{self.user.username}'s rating"
    
class ProcessedProducts(models.Model):
    img = CloudinaryField( 'products',
        default=config('CLD_URL'))
    product = models.OneToOneField(CoffeeProducts,on_delete=models.CASCADE)
    rating = models.ManyToManyField(Ratings)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name


class FarmerProfile(models.Model):
    farmer = models.OneToOneField(Farmer,on_delete=models.CASCADE)
    products = models.ManyToManyField(CoffeeProducts)
    
    def __str__(self):
        return self.farmer.username


