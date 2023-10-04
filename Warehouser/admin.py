from django.contrib import admin
from .models import Warehouse,ShippingManifest
# Register your models here.
admin.site.register(ShippingManifest)
admin.site.register(Warehouse)