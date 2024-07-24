from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Cart,Order,CartItem
from Authentication.models import Account
from .serializers import CartSerializers,OrderSerializers,CartItemSerializers
from Farming.models import ProcessedProducts
from Farming.serializers import ProductsSerializers,GetProcessedProductsSerializers
from Warehouser.models import Warehouse
from .cart_check import createCartForAnonymousUser

class ordersAndCart:
    class Anonymous:
        @api_view(["POST"])
        def addToCart(request,session,id):
            data = {}
            serializers = CartItemSerializers(data=request.data)
            if serializers.is_valid():
                item = serializers.save(id=id)
                cart = Cart.objects.get(session_id = session)
                cart.products.add(item)
                data = f"{item.product.product.name} has been added to your cart."
                return Response(data,status=status.HTTP_202_ACCEPTED)
            else:
                data = serializers.errors
                print(data)
                return Response(data,status=status.HTTP_400_BAD_REQUEST)
            
        @api_view(["DELETE"])
        def removeFromCart(request,session,id):
            data = {}
            item = CartItem.objects.get(id=id)
            cart = Cart.objects.get(session_id = session)
            cart.products.remove(item)
            data = f"{item.product.product.name} has been remove to your cart."
            return Response(data,status=status.HTTP_202_ACCEPTED)
        
        @api_view(["GET"])
        def addToWishlist(request,session,id):
            data = {}
            item = ProcessedProducts.objects.get(id=id)
            cart = Cart.objects.get(session_id = session)
            cart.wishlist.add(item)
            data = f"{item.product.name} has been added to your cart."
            return Response(data,status=status.HTTP_202_ACCEPTED)
            
            
        @api_view(["GET"])
        def removeFromWishlist(request,session,id):
            data = {}
            item = ProcessedProducts.objects.get(id=id)
            cart = Cart.objects.get(session_id = session)
            cart.wishlist.remove(item)
            data = f"{item.product.product.name} has been remove to your wishlist."
            return Response(data,status=status.HTTP_202_ACCEPTED)
    
    class Authenticated:
        @api_view(["POST"])
        @authentication_classes([JWTAuthentication])
        @permission_classes([IsAuthenticated])
        def addToCart(request,id):
            data = {}
            serializers = CartItemSerializers(data=request.data)
            if serializers.is_valid():
                item = serializers.save(id=id)
                buyer = Account.objects.get(id = request.user.id)
                cart = Cart.objects.get(buyer = buyer)
                cart.products.add(item)
                data = f"{item.product.product.name} has been added to your cart."
                return Response(data,status=status.HTTP_202_ACCEPTED)
            else:
                data = serializers.errors
                print(data)
                return Response(data,status=status.HTTP_400_BAD_REQUEST)
            
        @api_view(["GET"])
        @authentication_classes([JWTAuthentication])
        @permission_classes([IsAuthenticated])
        def removeFromCart(request,id):
            data = {}
            item = CartItem.objects.get(id=id)
            buyer = Account.objects.get(id = request.user.id)
            cart = Cart.objects.get(buyer = buyer)
            cart.products.remove(item)
            data = f"{item.product.product.name} has been remove to your cart."
            return Response(data,status=status.HTTP_202_ACCEPTED)
        
        @api_view(["GET"])
        @authentication_classes([JWTAuthentication])
        @permission_classes([IsAuthenticated])
        def addToWishlist(request,id):
            data = {}
            item = ProcessedProducts.objects.get(id=id)
            buyer = Account.objects.get(id = request.user.id)
            cart = Cart.objects.get(buyer = buyer)
            cart.wishlist.add(item)
            data = f"{item.product.name} has been added to your cart."
            return Response(data,status=status.HTTP_202_ACCEPTED)
            
            
        @api_view(["GET"])
        @authentication_classes([JWTAuthentication])
        @permission_classes([IsAuthenticated])
        def removeFromWishlist(request,id):
            data = {}
            item = ProcessedProducts.objects.get(id=id)
            buyer = Account.objects.get(id = request.user.id)
            cart = Cart.objects.get(buyer = buyer)
            cart.wishlist.remove(item)
            data = f"{item.product.product.name} has been remove to your wishlist."
            return Response(data,status=status.HTTP_202_ACCEPTED)

    @api_view(["GET"])
    def getCart(request):
        data = {}
        session = request.query_params.get('session')
        if session:
            try:
                cart = Cart.objects.get(session_id=session)
                data = CartSerializers(cart).data
                return Response(data, status=status.HTTP_200_OK)
            except:
                cart = Cart.objects.create(session_id=session)
                data = CartSerializers(cart).data
                return Response(data, status=status.HTTP_200_OK)
        else:
            cart = createCartForAnonymousUser(request=request)
            data = CartSerializers(cart).data
            return Response(data, status=status.HTTP_200_OK)
        
    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getAuthenticatedCart(request):
        data = {}
        cart = Cart.objects.get(buyer=request.user)
        data = CartSerializers(cart).data
        return Response(data,status=status.HTTP_200_OK)
    
    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def DeleteCart(request):
        data = {}
        Cart.delete_unclaimed_carts()
        data =  "Deletion successful"
        return Response(data,status=status.HTTP_200_OK)
        
    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getOrders(request):
        data = {}
        order = Order.objects.filter(buyer=request.user)
        data = OrderSerializers(order).data
        return Response(data,status=status.HTTP_200_OK)
    
    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getFarmerOrders(request):
        data = {}
        farmer_orders = []
        orders = Order.objects.all()
        for order in orders:
            for product in order.product.all():
                if product.product.product.producer == request.user:
                    if order not in farmer_orders:
                        farmer_orders.append(order)
                    else:
                        pass
        data = OrderSerializers(farmer_orders,many=True).data
        return Response(data,status=status.HTTP_200_OK)
    
    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getWarehouseOrders(request):
        data = {}
        try:
            warehouse = Warehouse.objects.get(warehouser=request.user)
            order = Order.objects.filter(
                warehouse=warehouse,
                is_paid=True
            )
            data = OrderSerializers(order,many=True).data
            return Response(data,status=status.HTTP_200_OK)
        except:
            return Response(data="None",status=status.HTTP_404_NOT_FOUND)
    
class Products:
    @api_view(["GET"])
    @authentication_classes([])
    @permission_classes([AllowAny])
    def getProducts(request):
        data = {}
        products = ProcessedProducts.objects.all()
        data = GetProcessedProductsSerializers(products,many=True).data
        return Response(data,status=status.HTTP_200_OK)
    
    @api_view(["GET"])
    @authentication_classes([])
    @permission_classes([AllowAny])
    def getProduct(request,id):
        data = {}
        products = ProcessedProducts.objects.get(id=id)
        data = GetProcessedProductsSerializers(products).data
        return Response(data,status=status.HTTP_200_OK)
    
    
        
    
