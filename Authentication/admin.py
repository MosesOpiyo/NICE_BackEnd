from django.contrib import admin
from .models import * 
# Register your models here.
admin.site.register(Admin)
admin.site.register(Farmer)
admin.site.register(Warehouser)
admin.site.register(Buyer)
admin.site.register(Profile)
admin.site.register(Account)