import binascii,os
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from Authentication.models import Buyer,Farmer,Warehouser,Account
from Authentication.serializers import AccountSerializer,FarmerRegistrationSerializer
from Depending_Accounts.models import Pending_Account
from Depending_Accounts.serializers import GetPendingSerializers
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
    def allPendingAccounts(request):
        data = {}
        if request.user.is_staff == True and request.user.is_admin == True and request.user.is_authenticated:
            accounts = Pending_Account.objects.all()
            data = GetPendingSerializers(accounts,many=True).data
            return Response(data=data,status=status.HTTP_200_OK)
        else:
            account = Account.objects.get(id=request.user.id)
            account.delete()

    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def validatePendingAccount(request,id):
        data = {}
        if request.user.is_staff == True and request.user.is_admin == True and request.user.is_authenticated:
            pending_account = Pending_Account.objects.get(id=id)
            account_data = {
                "email":pending_account.email,
                "username":pending_account.username,
                "password":binascii.hexlify(os.urandom(5)).decode('utf-8')
            }
            serializer = FarmerRegistrationSerializer(data=account_data)
            if serializer.is_valid():
                serializer.save()
                pending_account.delete()
                data = f"{serializer.data['username']}'s account has been temporarily activated. Waiting for password validation for full activation."
                return Response(data=data,status=status.HTTP_200_OK)
            else:
                data = serializer.errors
                print(serializer.errors)
                return Response(data=data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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


    

