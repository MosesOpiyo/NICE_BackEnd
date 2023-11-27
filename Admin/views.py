import binascii,os
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from Authentication.models import Buyer,Farmer,Warehouser,Account
from Authentication.serializers import AccountSerializer,FarmerRegistrationSerializer
from Farming.models import CoffeeProducts,ProcessedProducts
from Farming.serializers import ProcessedProductsSerializer,GetProcessedProductsSerializers
from .models import Requests
from .serializers import RequestsSerializers

# Create your views here.
class Admin:
    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def allBuyers(request):
        data = {}
        if request.user.is_staff == True and request.user.is_admin == True and request.user.is_authenticated:
            buyers = Buyer.objects.all()
            data = AccountSerializer(buyers,many=True).data
            return Response(data=data,status=status.HTTP_200_OK)

        else:
            account = Account.objects.get(id=request.user.id)
            account.delete()

    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def allFarmers(request):
        data = {}
        if request.user.is_staff == True and request.user.is_admin == True and request.user.is_authenticated:
           farmers = Farmer.objects.all()
           data = AccountSerializer(farmers,many=True).data
           return Response(data=data,status=status.HTTP_200_OK)
        else:
            account = Account.objects.get(id=request.user.id)
            account.delete()


    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def allWarehousers(request):
        data = {}
        if request.user.is_staff == True and request.user.is_admin == True and request.user.is_authenticated:
            warehousers = Warehouser.objects.all()
            data = AccountSerializer(warehousers,many=True).data
            return Response(data=data,status=status.HTTP_200_OK)
        else:
            account = Account.objects.get(id=request.user.id)
            account.delete()

    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def activeAdmins(request):
        data = {}
        if request.user.is_staff == True and request.user.is_admin == True and request.user.is_authenticated:
            active_admins = Account.objects.filter(type="ADMIN",is_admin=True,is_active=True,is_staff=True)
            data = AccountSerializer(active_admins,many=True).data
            return Response(data=data,status=status.HTTP_200_OK)
        else:
            account = Account.objects.get(id=request.user.id)
            account.delete()

    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def warehousingRequests(request):
        data = {}
        if request.user.is_staff == True and request.user.is_admin == True and request.user.is_authenticated:
            products = CoffeeProducts.objects.filter(requested_warehousing=True,warehouse_approved=False)
            data = AccountSerializer(products,many=True).data
            return Response(data=data,status=status.HTTP_200_OK)
        else:
            account = Account.objects.get(id=request.user.id)
            account.delete()

    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getProcessedProduct(request):
        data = {}
        products = ProcessedProducts.objects.all()
        data = GetProcessedProductsSerializers(products,many=True).data
        return Response(data,status=status.HTTP_200_OK)

    @api_view(["POST"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def addProcessedProduct(request):
        data = {}
        serializer = ProcessedProductsSerializer(data=request.data)

    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getProductRequest(request):
        data = {}
        requests = Requests.objects.all()
        data = RequestsSerializers(requests,many=True).data
        return Response(data,status=status.HTTP_200_OK)
    
    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def deleteUser(request,id):
        data = {}
        user = Account.objects.get(id=id)
        user.delete()
        data = f"user: {user.username} has been deleted."
        return Response(data,status=status.HTTP_200_OK)


    

