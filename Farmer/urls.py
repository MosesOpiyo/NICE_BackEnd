from django.urls import path
from Farmer import views as views

urlpatterns = [
    path("NewProduct",views.newProduct,name="new_product")
]