from django.urls import path
from Orders.views import ordersAndCart,Products

urlpatterns = [
    path("NewProductInCart/<int:id>",ordersAndCart.addToCart,name="new_product"),
    path("RemoveFromCart/<int:id>",ordersAndCart.removeFromCart,name="remove"),
    path("NewOrder",ordersAndCart.newOrder,name="new_order"), 
    path("Cart",ordersAndCart.getCart,name="cart"),
    path("Orders/q=orders",ordersAndCart.getOrders,name="orders"),
    path("FarmerOrders",ordersAndCart.getFarmerOrders,name="orders"),
    path("WarehouseOrders",ordersAndCart.getWarehouseOrders,name="orders"),
    path("Products",Products.getProducts,name="products"),
    path("Product/<int:id>",Products.getProduct,name="products")
]