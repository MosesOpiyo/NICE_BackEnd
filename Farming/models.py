from django.db import models
from cloudinary.models import CloudinaryField
from Authentication.models import Account,Buyer
from Pricing.models import Option
from datetime import datetime
from .mapping import field_mapping

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
    species = models.TextField(default="")
    acidity = models.TextField(default="")
    price = models.IntegerField(default=0)
    date = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField(default=0)
    requested_warehousing = models.BooleanField(default=False)
    shipment_successful = models.BooleanField(default=False)
    certification = models.TextField(default="")

    def __str__(self):
        return self.name
    
class Ratings(models.Model):
    user=models.ForeignKey(Buyer,on_delete=models.CASCADE)
    rating=models.IntegerField(default=0)
    comment=models.TextField(default="")

    def __str__(self):
        return f"{self.user.username}'s rating"
    
class ProcessedProducts(models.Model):
    img = CloudinaryField( 'products')
    product = models.ForeignKey(CoffeeProducts,on_delete=models.CASCADE)
    rating = models.ManyToManyField(Ratings)
    quantity = models.IntegerField(default=0)
    code = models.CharField(max_length=10,default="")
    pricing = models.ManyToManyField(Option)

    def __str__(self):
        return self.product.name


class FarmerProfile(models.Model):
    farmer = models.OneToOneField(Account,on_delete=models.CASCADE,unique=True,null=True)
    county = models.TextField(default="")
    country = models.TextField(default="")
    wet_mill_name = models.TextField(default="")
    estate_name = models.TextField(default="")
    estate_manager = models.TextField(default="")
    society_name = models.TextField(default="")
    factory_chairman = models.TextField(default="")
    factory_manager = models.TextField(default="")
    no_of_farmers = models.TextField(default="")
    male_farmers = models.TextField(default="")
    female_farmers = models.TextField(default="")
    total_acreage = models.TextField(default="")
    no_of_trees = models.TextField(default="")
    altitude = models.TextField(default="")
    harvest_season = models.TextField(default="")
    annual_rainfall = models.TextField(default="")
    annual_temp = models.TextField(default="")
    soil_type = models.TextField(default="")
    cupping_notes = models.TextField(default="")
    availability = models.TextField(default="")
    grower_history = models.TextField(default="")
    location = models.TextField(default="")
    farm_area = models.TextField(default=0)
    species = models.TextField(default="")
    varieties = models.TextField(default="")
    farming_method = models.TextField(default="")
    processing_method = models.TextField(default="")
    drying_method = models.TextField(default="")
    certification_type = models.TextField(default="")
    cherry_production_2019_to_2020 = models.TextField(default="")
    cherry_production_2020_to_2021 = models.TextField(default="")
    cherry_production_2021_to_2022 = models.TextField(default="")
    
    def __str__(self):
        return str(self.id)
    
    def create_farmer_profile(data):
        # Map incoming data to model fields
        mapped_data = {}
        for key, model_field in field_mapping.items():
            if key in data:
                value = data[key]

                # if model_field in ["no_of_farmers", "male_farmers", "female_farmers", "total_acreage", "no_of_trees"]:
                #     value = value.replace(",", "") if isinstance(value, str) else value
                #     value = int(value) if value else 0
                
                if model_field in ["annual_rainfall", "annual_temp", "altitude"]:
                    value = value.replace("mm", "").replace("?c", "").replace(",", "").strip() if isinstance(value, str) else value
                
                mapped_data[model_field] = value or ""  # Use empty string if value is missing

        # Handle extra fields like 'farm_area' if needed
        mapped_data["farm_area"] = int(mapped_data.get("total_acreage", 0))  # Example logic for `farm_area`

        # Create FarmerProfile object
        farmer_profile = FarmerProfile.objects.create(**mapped_data)
        return farmer_profile


class Stories(models.Model):
    media = CloudinaryField("/stories")
    caption = models.TextField(default="")
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=datetime(2023, 1, 1, 12, 0, 0))

    def __str__(self):
        return str(self.id)
