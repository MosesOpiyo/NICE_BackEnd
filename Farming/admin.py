from django.contrib import admin
from .models import FarmerProfile,ProcessedProducts,Ratings

# Register your models here.
admin.site.register(FarmerProfile)
admin.site.register(ProcessedProducts)
admin.site.register(Ratings)