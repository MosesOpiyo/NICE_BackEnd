import random,binascii,os
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CoffeeProducts,ProcessedProducts
from Warehouser.models import ShippingManifest,Warehouse
from .serializers import ProductsSerializers,RatingSerializers,GetProcessedProductsSerializers


# Create your views here.
class Farming:
    @api_view(["POST"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def newProduct(request):
        data = {}
        warehouses = Warehouse.objects.all()
        random_warehouse = random.choice(warehouses)
        serializers = ProductsSerializers(data=request.data)
        if serializers.is_valid():
            product = serializers.save(request)
            name = product.name
            manifest = ShippingManifest.objects.create(
                number = binascii.hexlify(os.urandom(5)).decode('utf-8'),
                product = product,
                warehouser = random_warehouse.warehouser
                )
            manifest.save()
            data = f"New Product {name}and Manifest for {manifest.product.name} created."
            return Response(data,status=status.HTTP_201_CREATED)
        else:
            data = serializers.error_messages
            Response(data,status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getProducts(request):
        data = {}
        products = CoffeeProducts.objects.select_related('producer').filter(producer=request.user)
        data =  ProductsSerializers(products,many=True).data
        return Response(data,status = status.HTTP_200_OK)
    
    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getRequestedProducts(request):
        data = {}
        products = CoffeeProducts.objects.select_related('producer').filter(producer=request.user,requested_warehousing=True)
        data =  ProductsSerializers(products,many=True).data
        return Response(data,status = status.HTTP_200_OK)
    
    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getShippingProducts(request):
        data = {}
        products = CoffeeProducts.objects.select_related('producer').filter(requested_warehousing=True)
        data =  ProductsSerializers(products,many=True).data
        return Response(data,status = status.HTTP_200_OK)
    
class Processed:
    @api_view(['POST'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def productRating(request,id):
        data = {}
        serializers = RatingSerializers(data=request.data)
        product = ProcessedProducts.objects.prefetch_related('rating').select_related('product').get(id=id)
        if serializers.is_valid():
            rating = serializers.save(request)
            product.rating.add(rating)
            product.save()
            return Response(data,status=status.HTTP_201_CREATED)
        else:
            data = serializers.error_messages
            Response(data,status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getProducts(request):
        data = {}
        products = ProcessedProducts.objects.prefetch_related('rating').select_related('product').all()
        data = GetProcessedProductsSerializers(products,many=True).data
        return Response(data,status = status.HTTP_200_OK)  
    
    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getProduct(request,id):
        data = {}
        product = ProcessedProducts.objects.prefetch_related('rating').select_related('product').get(id=id)
        data = GetProcessedProductsSerializers(product).data
        return Response(data,status = status.HTTP_200_OK)  
    