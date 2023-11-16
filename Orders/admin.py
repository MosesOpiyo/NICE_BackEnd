from django.contrib import admin
from .models import Cart,Order,CoffeeProducts,CartItem

# Register your models here.
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(CoffeeProducts)
admin.site.register(CartItem)
