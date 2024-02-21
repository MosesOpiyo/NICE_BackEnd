from django.urls import path
from Orders.views import ordersAndCart,Products

urlpatterns = [
    path("NewProductInCart/<str:session>/<int:id>",ordersAndCart.addToCart,name="new_product"),
    path("RemoveFromCart/<str:session>/<int:id>",ordersAndCart.removeFromCart,name="remove"),
    path("NewProductInWishList/<str:session>/<int:id>",ordersAndCart.addToWishlist,name="new_wishlist_product"),
    path("RemoveFromWishlist/<str:session>/<int:id>",ordersAndCart.removeFromWishlist,name="wishlist_remove"),
    path("NewOrder",ordersAndCart.newOrder,name="new_order"), 
    path("Cart",ordersAndCart.getCart,name="cart"),
    path("Orders/q=orders",ordersAndCart.getOrders,name="orders"),
    path("FarmerOrders",ordersAndCart.getFarmerOrders,name="orders"),
    path("WarehouseOrders",ordersAndCart.getWarehouseOrders,name="orders"),
    path("Products",Products.getProducts,name="products"),
    path("Product/<int:id>",Products.getProduct,name="products")
]