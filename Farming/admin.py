from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(FarmerProfile)
admin.site.register(ProcessedProducts)
admin.site.register(Ratings)
admin.site.register(Stories)