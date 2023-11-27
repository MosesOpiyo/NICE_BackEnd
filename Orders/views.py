from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Cart,Order,CartItem
from .serializers import CartSerializers,OrderSerializers,CartItemSerializers
from Farming.models import ProcessedProducts
from Farming.serializers import ProductsSerializers,GetProcessedProductsSerializers
from Warehouser.models import Warehouse

class ordersAndCart:
    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def removeToCart(request,id):
        data = {}
        product = ProcessedProducts.objects.get(id=id)
        cart = Cart.objects.get(buyer = request.user)
        cart.products.remove(product)
        data = f"{product.product.name} has been removed to your cart."
        return Response(data,status=status.HTTP_202_ACCEPTED)
    
    @api_view(["POST"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def addToCart(request,id):
        data = {}
        serializers = CartItemSerializers(data=request.data)
        if serializers.is_valid():
            item = serializers.save(id=id)
            cart = Cart.objects.get(buyer = request.user)
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
        cart = Cart.objects.get(buyer = request.user)
        cart.products.remove(item)
        data = f"{item.product.product.name} has been remove to your cart."
        return Response(data,status=status.HTTP_202_ACCEPTED)
        
    @api_view(["POST"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def newOrder(request):
        data = {}
        product_serializer = ProductsSerializers(data=request.data)
        if product_serializer.is_valid():
            order = Order.objects.create(buyer=request.user)
            if order:
                order.product = product_serializer
                order.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                new_order = Order.objects.create(
                    buyer = request.user
                )
                new_order = product_serializer
                new_order.save()
                return Response(status=status.HTTP_202_ACCEPTED)
        else:
            data = product_serializer.error_messages
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        

    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getCart(request):
        data = {}
        cart = Cart.objects.get(buyer=request.user)
        data = CartSerializers(cart).data
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
    def getWarehouseOrders(request):
        data = {}
        warehouse = Warehouse.objects.get(warehouser=request.user)
        order = Order.objects.filter(warehouse=warehouse)
        data = OrderSerializers(order,many=True).data
        return Response(data,status=status.HTTP_200_OK)
    
class Products:
    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getProducts(request):
        data = {}
        products = ProcessedProducts.objects.all()
        data = GetProcessedProductsSerializers(products,many=True).data
        return Response(data,status=status.HTTP_200_OK)
    
    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getProduct(request,id):
        data = {}
        products = ProcessedProducts.objects.get(id=id)
        data = GetProcessedProductsSerializers(products).data
        return Response(data,status=status.HTTP_200_OK)
        
    
