from django.urls import path
from Orders.views import ordersAndCart

urlpatterns = [
    path("NewProductInCart",ordersAndCart.addToCart,name="new_product"),
    path("NewOrder",ordersAndCart.newOrder,name="new_order"),
    path("Cart/<int:pk>/q=cart_products",ordersAndCart.getCart,name="cart"),
    path("orders/<int:pk>/q=orders",ordersAndCart.getOrders,name="orders"),
]