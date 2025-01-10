from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

import json
from .models import Cart,Order,CartItem,Sample
from Authentication.models import Account
from .serializers import CartSerializers,GetOrderSerializers,OrderSerializer,CartItemSerializers,UpdateCartItemsSerializers,SampleSerializers
from Farming.models import ProcessedProducts
from Farming.serializers import ProductsSerializers,GetProcessedProductsSerializers
from Warehouser.models import Warehouse
from .cart_check import createCartForAnonymousUser
from Farming.redis import large_processed_products_view

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
                return Response(data,status=status.HTTP_400_BAD_REQUEST)
            
        @api_view(["DELETE"])
        def removeFromCart(request,session,id):
            data = {}
            item = CartItem.objects.get(id=id)
            cart = Cart.objects.get(session_id = session)
            cart.products.remove(item)
            item.delete()
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
        
        @api_view(["POST"])
        def addSample(request,session,id):
            data = {}
            serializers = SampleSerializers(data=request.data)
            if serializers.is_valid():
                sample = serializers.save(id=id)
                cart = Cart.objects.get(session_id = session)
                cart.samples.add(sample)
                data = f"{sample.product.product.name} Sample has been added to your cart."
                return Response(data,status=status.HTTP_202_ACCEPTED)
            else:
                data = serializers.errors
                return Response(data,status=status.HTTP_400_BAD_REQUEST)
            
        @api_view(["GET"])
        def removeSample(request,id):
            data = {}
            buyer = Account.objects.get(id = request.user.id)
            cart = Cart.objects.get(buyer = buyer)
            sample = Sample.objects.get(id = id)
            cart.samples.remove(sample)
            sample.delete()
            data = f"{sample.product.product.name} Sample has been removed to your cart."
            return Response(data,status=status.HTTP_202_ACCEPTED)
            
            
        @api_view(["GET"])
        def removeFromWishlist(request,session,id):
            data = {}
            item = ProcessedProducts.objects.get(id=id)
            cart = Cart.objects.get(session_id = session)
            cart.wishlist.remove(item)
            item.delete()
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
            
        @api_view(["PUT"])
        @authentication_classes([JWTAuthentication])
        @permission_classes([IsAuthenticated])
        def updateCartItems(request):
            cart_items_data = request.data.get('items')
            cart_items_data = json.loads(cart_items_data)
            for item_data in cart_items_data:
                cart_item = get_object_or_404(CartItem, id=item_data['id'])
                serializer = UpdateCartItemsSerializers(cart_item, data=item_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"detail": "Cart items updated successfully"}, status=status.HTTP_200_OK)

            
        @api_view(["GET"])
        @authentication_classes([JWTAuthentication])
        @permission_classes([IsAuthenticated])
        def removeFromCart(request,id):
            data = {}
            item = CartItem.objects.get(id=id)
            buyer = Account.objects.get(id = request.user.id)
            cart = Cart.objects.get(buyer = buyer)
            cart.products.remove(item)
            item.delete()
            data = f"{item.product.product.name} has been removed to your cart."
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
            item.delete()
            data = f"{item.product.product.name} has been removed to your wishlist."
            return Response(data,status=status.HTTP_202_ACCEPTED)
        
        @api_view(["POST"])
        @authentication_classes([JWTAuthentication])
        @permission_classes([IsAuthenticated])
        def addSample(request,id):
            data = {}
            serializers = SampleSerializers(data=request.data)
            if serializers.is_valid():
                sample = serializers.save(id=id)
                buyer = Account.objects.get(id = request.user.id)
                cart = Cart.objects.get(buyer = buyer)
                cart.samples.add(sample)
                data = f"{sample.product.product.name} Sample has been added to your cart."
                return Response(data,status=status.HTTP_202_ACCEPTED)
            else:
                data = serializers.errors
                return Response(data,status=status.HTTP_400_BAD_REQUEST)
            
        @api_view(["GET"])
        @authentication_classes([JWTAuthentication])
        @permission_classes([IsAuthenticated])
        def removeSample(request,id):
            data = {}
            buyer = Account.objects.get(id = request.user.id)
            cart = Cart.objects.get(buyer = buyer)
            sample = Sample.objects.get(id = id)
            cart.samples.remove(sample)
            sample.delete()
            data = f"{sample.product.product.name} Sample has been removed to your cart."
            return Response(data,status=status.HTTP_202_ACCEPTED)
        

        @api_view(["POST"])
        @authentication_classes([JWTAuthentication])
        @permission_classes([IsAuthenticated])
        def buyNow(request,id):
            data = {}

            delivery_data = json.loads(request.data.get('delivery'))
            payment_data = json.loads(request.data.get('payment'))
            billing_data = json.loads(request.data.get('billing'))
            product_data = json.loads(request.data.get('product'))

            form_data = {
                'delivery': delivery_data,
                'payment': payment_data,
                'billing': billing_data,
                'product':product_data

            }
            serializers = OrderSerializer(data=form_data)
            if serializers.is_valid():
                status_code,url = serializers.create_order_items(id=id,request=request,validated_data=form_data)
                if status_code == 200:
                    redirect = url
                    print(redirect)
                    return Response(redirect,status=status.HTTP_201_CREATED)
                else:
                    msg = "Payment cancelled."
                    return Response(msg,status=status.HTTP_400_BAD_REQUEST)
            else:
                data = serializers.errors
                print(data)
                return Response(data,status=status.HTTP_400_BAD_REQUEST)
            
        @api_view(["POST"])
        @authentication_classes([JWTAuthentication])
        @permission_classes([IsAuthenticated])
        def CartCheckOut(request):
            data = {}
            delivery_data = json.loads(request.data.get('delivery'))
            payment_data = json.loads(request.data.get('payment'))
            billing_data = json.loads(request.data.get('billing'))

            form_data = {
                'delivery': delivery_data,
                'payment': payment_data,
                'billing': billing_data,

            }
            serializers = OrderSerializer(data=form_data)
            if serializers.is_valid():
                status_code,url = serializers.create_cart_items(id=request.user.id,validated_data=form_data)
                if status_code == 200:
                    redirect = url
                    return Response(redirect,status=status.HTTP_201_CREATED)
                else:
                    msg = "Payment cancelled."
                    return Response(msg,status=status.HTTP_400_BAD_REQUEST)
            else:
                data = serializers.errors
                print(data)
                return Response(data,status=status.HTTP_400_BAD_REQUEST)
            
        @api_view(["GET"])
        @authentication_classes([JWTAuthentication])
        @permission_classes([IsAuthenticated])
        def deleteNow(request):
            data = {}
            orders = Order.objects.all()
            orders.delete()
            return Response(data,status=status.HTTP_200_OK)

        @api_view(["POST"])
        @authentication_classes([JWTAuthentication])
        @permission_classes([IsAuthenticated])
        def addRating(request,id):
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
    def getCart(request):

        session = request.query_params.get('session')
        if not session:
            cart = createCartForAnonymousUser(request=request)
            data = CartSerializers(cart).data
            return Response(data, status=status.HTTP_200_OK)
        
        try:
            cart, created = Cart.objects.get_or_create(session_id=session)
            data = CartSerializers(cart).data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(
                    {"error": "Failed to retrieve or create cart.", "details": str(error)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        
    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getAuthenticatedCart(request):
        data = {}
        try:
            cart = Cart.objects.get(buyer=request.user)
            data = CartSerializers(cart).data
            return Response(data,status=status.HTTP_200_OK)
        except:
            data = "Cart has not been found"
            return Response(data,status=status.HTTP_404_NOT_FOUND)
    
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
        order = Order.objects.all()
        data = GetOrderSerializers(order,many=True).data
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
        data = OrderSerializer(farmer_orders,many=True).data
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
            data = OrderSerializer(order,many=True).data
            return Response(data,status=status.HTTP_200_OK)
        except:
            return Response(data="None",status=status.HTTP_404_NOT_FOUND)
    
class Products:
    @api_view(["GET"])
    @authentication_classes([])
    @permission_classes([AllowAny])
    def getProducts(request):
        data = {}
        products = ProcessedProducts.objects.prefetch_related('rating').select_related('product').filter(pricing__isnull=False).distinct()
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
    
    
    
        
    
