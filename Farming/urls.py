from django.urls import path
from Farming.views import Farming

urlpatterns = [
    path("NewProduct",Farming.newProduct,name="new_product"),
    path("FarmerProduct",Farming.getProducts,name="products"),
]