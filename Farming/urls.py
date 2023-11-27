from django.urls import path
from Farming.views import *

urlpatterns = [
    path("NewProduct",Farming.newProduct,name="new_product"),
    path("NewProcessedProduct/<int:id>",Farming.newProcessedProduct,name="new_processed_product"),
    path("FarmerProduct",Farming.getProducts,name="products"),
    path("FarmerProfile",Farming.getProfile,name="profile"),
    path("FarmerProfileDetails",Farming.newProfileDetails,name="profile_details"),
    path("FarmerRequestedProduct",Farming.getRequestedProducts,name="requested_products"),
    path("ShippingProduct",Farming.getShippingProducts,name="shipping_products"),
    path("getProducts",Processed.getProducts,name="products"),
    path("getProduct/<int:id>",Processed.getProduct,name="product"),
    path("ProductRequest",ProductRequests.request,name="product_request"),
    path("Story",Story.newStory,name="story"),
]