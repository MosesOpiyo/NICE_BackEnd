from django.contrib import admin
from .models import Address,Receipt,Subscription
# Register your models here.
admin.site.register(Address)
admin.site.register(Receipt)
admin.site.register(Subscription)