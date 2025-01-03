from django.contrib import admin
from .models import Cart,Billing,Payment,Delivery,ProductOrder,Order,CoffeeProducts,CartItem,Sample

# Register your models here.
admin.site.register(Cart)
admin.site.register(Billing)
admin.site.register(Payment)
admin.site.register(Delivery)
admin.site.register(ProductOrder)
admin.site.register(Order)
admin.site.register(CoffeeProducts)
admin.site.register(CartItem)
admin.site.register(Sample)
