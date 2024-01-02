import binascii,os
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from cloudinary.uploader import upload

from NICE_BACK.image import compress_image
from .models import Warehouse,ShippingManifest
from Authentication.models import Warehouser,Account
from Authentication.serializers import UserSerializer
from Farming.models import CoffeeProducts,ProcessedProducts
from Notifications.models import Notification
from .serializers import WarehouseSerializers,GetWarehouseSerializers,ShippingManifestSerializers,GetShippingManifestSerializers
from Farming.serializers import ProductsSerializers,ProcessedProductsSerializer

class WarehouseClass:
    @api_view(["POST"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def createWareHouse(request):
        data = {}
        serializer = WarehouseSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = "New warehouse created"
            return Response(data,status=status.HTTP_201_CREATED)
        
    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def get_warehouse(request):
        data = {}
        try:
            warehouse = Warehouse.objects.select_related('warehouser').prefetch_related('warehoused_products').get(warehouser=request.user)
            try:
                data =  GetWarehouseSerializers(warehouse).data
                return Response(data,status = status.HTTP_200_OK)
            except:
                new_warehouse = Warehouse.objects.create(
                   warehouser = request.user
                )
                data = GetWarehouseSerializers(new_warehouse).data
                return Response(data,status = status.HTTP_200_OK)
        except:
            if request.user.type == "ORIGINWAREHOUSER":
                try:
                    warehouse = Warehouse.objects.select_related('warehouser').prefetch_related('warehoused_products').get(name='NICE WAREHOUSE')
                    data =  GetWarehouseSerializers(warehouse).data
                    return Response(data,status = status.HTTP_200_OK)
                except:
                    new_warehouse = Warehouse.objects.create(
                    name='NICE WAREHOUSE'
                    )
                    data = GetWarehouseSerializers(new_warehouse).data
                    return Response(data,status = status.HTTP_200_OK)
            else:
                new_warehouse = Warehouse.objects.create(
                   name = f"{request.user}'s Warehouse",
                   warehouser = request.user
                )
                data = GetWarehouseSerializers(new_warehouse).data
                return Response(data,status = status.HTTP_200_OK)
            
    @api_view(['PUT'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def updateProfile(request,key):
        data_update = request.data.get(f"{key}")
        warehouse = Warehouse.objects.get(warehouser=request.user)
        serializer = GetWarehouseSerializers(warehouse)
        serialized_data = serializer.data
        for attribute in serialized_data.keys():
            if attribute == key:
                serialized_data[key] = data_update

        updated_serializer = GetWarehouseSerializers(warehouse,data=serialized_data)
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
    def get_warehouse_products(request):
        data = {}
        products = CoffeeProducts.objects.select_related('producer').all()
        data =  ProductsSerializers(products,many=True).data
        return Response(data,status = status.HTTP_200_OK)
    

class shippingClass:
    @api_view(['POST'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def createManifest(request,id):
        data = {}
        serializer = ShippingManifestSerializers(data=request.data)
        if serializer.is_valid():
            manifest = serializer.save(id=id)
            notification_data = Notification.objects.create(message=f"Product:{manifest.product} of Manifest:{manifest.number} set for shipping to your warehouse")
            warehouser = Account.objects.get(email=manifest.warehouser)
            warehouser.notifications.add(notification_data)
        return Response(data,status=status.HTTP_200_OK)
    
    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getManifests(request):
        data = {}
        manifests = ShippingManifest.objects.select_related('product').all()
        data = GetShippingManifestSerializers(manifests,many=True).data
        return Response(data,status=status.HTTP_200_OK)
    
    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getWarehousers(request):
        data = {}
        warehousers = Warehouser.objects.all()
        data = UserSerializer(warehousers,many=True).data
        return Response(data,status=status.HTTP_200_OK)

    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def shipToWarehouser(request,id):
        data = {}
        manifest = ShippingManifest.objects.get(id=id)
        manifest.shipping_approval = True
        manifest.save()
        data = "Shipping Set"
        return Response(data,status=status.HTTP_200_OK)
    
class shippedClass:
    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getManifest(request,number):
        data = {}
        manifest = ShippingManifest.objects.select_related('product').get(number=number)
        warehouse = Warehouse.objects.select_related('warehouser').prefetch_related('warehoused_products','processed_products').get(warehouser=request.user)
        warehouse.warehoused_products.add(manifest)
        assets_folder = 'assets'
        for image_name in os.listdir(assets_folder):
            image_path = os.path.join(assets_folder, image_name)
            try:
                cloudinary_response = upload(image_path)
                cloudinary_url = cloudinary_response['url'].replace('http://res.cloudinary.com/dlzyg12i7/', '')
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            product_data = {'img': cloudinary_url,'quantity':0}
            product_serializer = ProcessedProductsSerializer(data=product_data)
            if product_serializer.is_valid():
                product_serializer.save(id=manifest.product.pk,request=request)
            else:
                return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            
        warehouse.save()
        data = f"{manifest.product} has been added to your inventory."
        notification = Notification.objects.create(
            message=data
        )
        warehouse.warehouser.notifications.add(notification)
        return Response(data,status=status.HTTP_200_OK)
        