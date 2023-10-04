from django.urls import path
from Orders.views import ordersAndCart

urlpatterns = [
    path("NewProductInCart",ordersAndCart.addToCart,name="new_product"),
    path("NewOrder",ordersAndCart.newOrder,name="new_order"),
    path("Cart/q=cart_products",ordersAndCart.getCart,name="cart"),
    path("Orders/q=orders",ordersAndCart.getOrders,name="orders"),
    path("WarehouseOrders",ordersAndCart.getWarehouseOrders,name="orders"),
]