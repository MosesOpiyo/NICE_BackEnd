from django.urls import path
from Orders.views import ordersAndCart,Products

urlpatterns = [
    path("NewProductInCart/<str:session>/<int:id>",ordersAndCart.Anonymous.addToCart,name="new_product"),
    path("RemoveFromCart/<str:session>/<int:id>",ordersAndCart.Anonymous.removeFromCart,name="remove"),
    path("NewProductInWishList/<str:session>/<int:id>",ordersAndCart.Anonymous.addToWishlist,name="new_wishlist_product"),
    path("RemoveFromWishlist/<str:session>/<int:id>",ordersAndCart.Anonymous.removeFromWishlist,name="wishlist_remove"),
    path("NewSample/<str:session>/<int:id>",ordersAndCart.Anonymous.addSample,name="new_sample"),
    path("RemoveSample/<str:session>/<int:id>",ordersAndCart.Anonymous.removeSample,name="remove_sample"),
    path("NewProductInCart/<int:id>",ordersAndCart.Authenticated.addToCart,name="new_product"),
    path("UpdateCartItems",ordersAndCart.Authenticated.updateCartItems,name="update"),
    path("RemoveFromCart/<int:id>",ordersAndCart.Authenticated.removeFromCart,name="remove"),
    path("NewProductInWishList/<int:id>",ordersAndCart.Authenticated.addToWishlist,name="new_wishlist_product"),
    path("RemoveFromWishlist/<int:id>",ordersAndCart.Authenticated.removeFromWishlist,name="wishlist_remove"),
    path("NewSample/<int:id>",ordersAndCart.Authenticated.addSample,name="new_sample"),
    path("RemoveSample/<int:id>",ordersAndCart.Authenticated.removeSample,name="remove_sample"),
    path("CartCheckOut",ordersAndCart.Authenticated.CartCheckOut,name="cart_checkout"),
    path("BuyNow/<int:id>",ordersAndCart.Authenticated.buyNow,name="buy_now"),
    path("DeleteNow",ordersAndCart.Authenticated.deleteNow,name="delete_now"),
    path("RemoveCarts",ordersAndCart.DeleteCart,name="remove"),
    path("Cart",ordersAndCart.getCart,name="cart"),
    path("AuthenticatedCart",ordersAndCart.getAuthenticatedCart,name="cart"),
    path("Orders/q=orders",ordersAndCart.getOrders,name="orders"),
    path("FarmerOrders",ordersAndCart.getFarmerOrders,name="orders"),
    path("WarehouseOrders",ordersAndCart.getWarehouseOrders,name="orders"),
    path("Products",Products.getProducts,name="products"),
    path("Product/<int:id>",Products.getProduct,name="products")
]