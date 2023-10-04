from django.urls import path
from Farming.views import Farming,Processed

urlpatterns = [
    path("NewProduct",Farming.newProduct,name="new_product"),
    path("FarmerProduct",Farming.getProducts,name="products"),
    path("FarmerRequestedProduct",Farming.getRequestedProducts,name="requested_products"),
    path("ShippingProduct",Farming.getShippingProducts,name="shipping_products"),
    path("getProducts",Processed.getProducts,name="products"),
    path("getProduct/<int:id>",Processed.getProduct,name="product"),
    
]