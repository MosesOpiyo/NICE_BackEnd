from django.db import models
from cloudinary.models import CloudinaryField
from Authentication.models import Account,Farmer,Buyer
from decouple import config
from datetime import datetime

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
    img = CloudinaryField( 'products')
    product = models.ForeignKey(CoffeeProducts,on_delete=models.CASCADE)
    rating = models.ManyToManyField(Ratings)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    code = models.CharField(max_length=10,default="")

    def __str__(self):
        return self.product.name


class FarmerProfile(models.Model):
    farmer = models.OneToOneField(Account,on_delete=models.CASCADE,unique=True)
    county = models.TextField(default="")
    country = models.TextField(default="")
    wet_mill_name = models.TextField(default="")
    estate_name = models.TextField(default="")
    society_name = models.TextField(default="")
    factory_chairman = models.TextField(default="")
    factory_manager = models.TextField(default="")
    no_of_farmers = models.TextField(default="")
    men = models.TextField(default="")
    women = models.TextField(default="")
    total_acreage = models.TextField(default="")
    no_of_trees = models.TextField(default="")
    altitude = models.TextField(default="")
    harvest_season = models.TextField(default="")
    annual_rainfall_amount = models.TextField(default="")
    coffee_variety = models.TextField(default="")
    farming_method = models.TextField(default="")
    certification_type = models.TextField(default="")
    soil_type = models.TextField(default="")
    processing_method = models.TextField(default="")
    cupping_notes = models.TextField(default="")
    availability = models.TextField(default="")
    grower_history = models.TextField(default="")
    location = models.TextField(default="")
    farm_area = models.IntegerField(default=0)
    
    def __str__(self):
        return self.farmer.username


class Stories(models.Model):
    media = CloudinaryField("/stories")
    caption = models.TextField(default="")
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=datetime(2023, 1, 1, 12, 0, 0))

    def __str__(self):
        return str(self.id)
