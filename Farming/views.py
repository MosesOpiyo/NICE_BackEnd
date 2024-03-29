import random,binascii,os
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from Authentication.models import Account
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from Notifications.views import Notifications
from Warehouser.models import ShippingManifest,Warehouse
from .serializers import *


# Create your views here.
class Farming:
    @api_view(["POST"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def newProduct(request):
        data = {}
        serializers = ProductsSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save(request)
            return Response(data,status=status.HTTP_201_CREATED)
        else:
            data = serializers.errors
            print(data)
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(["POST"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def newProcessedProduct(request,id):
        data = {}
        serializers = ProcessedProductsSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(id=id,request=request)
            return Response(data,status=status.HTTP_201_CREATED)
        else:
            data = serializers.error_messages
            return Response(data,status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getProducts(request):
        data = {}
        products = CoffeeProducts.objects.select_related('producer').filter(producer=request.user)
        data =  ProductsSerializers(products,many=True).data
        return Response(data,status = status.HTTP_200_OK)
    
    @api_view(["POST"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def newProfileDetails(request):
        data = {}
        serializers = ProfileSerializers(data=request.data)
        if serializers.is_valid():
            details = serializers.save(request)
            data = f"Details for {details.farmer}'s Farm have been added."
            return Response(data=data,status=status.HTTP_202_ACCEPTED)
        else:
            print(serializers.data)
            data = serializers.errors
            print(data)
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getProfile(request):
        data = {}
        try:
            profile = FarmerProfile.objects.get(farmer=request.user)
            data =  GetProfileSerializers(profile).data
            return Response(data,status = status.HTTP_200_OK)
        except:
            data = ""
            return Response(data,status = status.HTTP_200_OK)
        
    @api_view(['PUT'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def updateProfile(request,key):
        data_update = request.data.get(f"{key}")
        farmer = FarmerProfile.objects.get(farmer=request.user)
        serializer = GetProfileSerializers(farmer)
        serialized_data = serializer.data
        for attribute in serialized_data.keys():
            if attribute == key:
                serialized_data[key] = data_update

        updated_serializer = GetProfileSerializers(farmer,data=serialized_data)
        if updated_serializer.is_valid():
            updated_serializer.save()
            return Response(data="Updated",status = status.HTTP_200_OK)
        else:
            data = updated_serializer.errors
            print(data)   
            return Response(data,status = status.HTTP_500_INTERNAL_SERVER_ERROR)

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

from Admin.models import Requests
from Authentication.email import send_welcome_email

class ProductRequests:
    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def request(request):
        new_request = Requests.objects.create(
            user=request.user
        )
        send_welcome_email(name=request.user.username,receiver=request.user.email)
        return Response(data="Request is being processed.",status=status.HTTP_200_OK)
        

class Excel:
    @api_view(["POST"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def farmerCreationInBulk(request):
        data = {}
        serializers = ProfileSerializers(data=request.data)
        product = ProcessedProducts.objects.prefetch_related('rating').select_related('product').get(id=id)
        if serializers.is_valid():
            rating = serializers.save(request)
            product.rating.add(rating)
            product.save()
            return Response(data,status=status.HTTP_201_CREATED)
        else:
            data = serializers.error_messages
            Response(data,status=status.HTTP_400_BAD_REQUEST) 


class Story:
    @api_view(["POST","GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def newStory(request):
        data = {}
        if request.method == "POST":
            serializers = StoriesSerializer(data=request.data)
            if serializers.is_valid():
                serializers.save(request=request)
                return Response(data,status=status.HTTP_201_CREATED)
            else:
                data = serializers.error_messages
                print(serializers.errors)
                return Response(data,status=status.HTTP_400_BAD_REQUEST)
        elif request.method == "GET":
            stories = Stories.objects.filter(user=request.user)
            data = GetStoriesSerializer(stories,many=True).data
            return Response(data,status = status.HTTP_200_OK)  

