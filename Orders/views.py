from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Cart,Order
from .serializers import CartSerializers,OrderSerializers
from Farming.models import ProcessedProducts
from Farming.serializers import ProductsSerializers
from Warehouser.models import Warehouse

class ordersAndCart:
    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def addToCart(request):
        data = {}
        product_serializer = ProductsSerializers(data=request.data)
        if product_serializer.is_valid():
            cart = Cart.objects.get(buyer=request.user)
            if cart:
                cart.products.add(product_serializer)
                cart.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                new_cart = Cart.objects.create(
                    buyer = request.user
                )
                new_cart.products.add(product_serializer)
                new_cart.save()
                return Response(status=status.HTTP_202_ACCEPTED)
        else:
            data = product_serializer.error_messages
            return Response(status=status.HTTP_400_BAD_REQUEST)


    @api_view(["POST"])
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
    @permission_classes([IsAuthenticated])
    def getCart(request):
        data = {}
        cart = Cart.objects.get(buyer=request.user)
        data = CartSerializers(cart).data
        return Response(data,status=status.HTTP_200_OK)
    
    @api_view(["GET"])
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
        order = Order.objects.filter()
        data = OrderSerializers(order,many=True).data
        return Response(data,status=status.HTTP_200_OK)
        
    
