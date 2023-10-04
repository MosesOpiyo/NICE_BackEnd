from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Warehouse,ShippingManifest
from Notifications.views import Notifications
from Farming.models import CoffeeProducts
from .serializers import WarehouseSerializers,GetWarehouseSerializers,ShippingManifestSerializers
from Farming.serializers import ProductsSerializers

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
            if warehouse:
                data =  GetWarehouseSerializers(warehouse).data
                return Response(data,status = status.HTTP_200_OK)
            else:
                new_warehouse = Warehouse.objects.create(
                   warehouser = request.user
                )
                data = GetWarehouseSerializers(new_warehouse).data
                return Response(data,status = status.HTTP_200_OK)
        except:
            warehouse = Warehouse.objects.select_related('warehouser').prefetch_related('warehoused_products').get(name='NICE WAREHOUSE')
            data =  GetWarehouseSerializers(warehouse).data
            return Response(data,status = status.HTTP_200_OK)
    
    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def get_warehouse_products(request):
        data = {}
        products = CoffeeProducts.objects.select_related('producer').all()
        data =  ProductsSerializers(products,many=True).data
        return Response(data,status = status.HTTP_200_OK)
    

class shippingClass:
    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getManifests(request):
        data = {}
        manifests = ShippingManifest.objects.select_related('warehouser','product').all()
        data = ShippingManifestSerializers(manifests,many=True).data
        return Response(data,status=status.HTTP_200_OK)

    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def shipToWarehouser(request,id):
        data = {}
        manifest = ShippingManifest.objects.get(id=id)
        manifest.shipping_approval = True
        manifest.save()
        notification_data = {
           "title": "Manifest Approval",
           "body":f"Product:{manifest.product} of Manifest:{manifest.number} set for shipping to your warehouse"
        }
        Notifications.send_notification_to_user(user_index=manifest.warehouser.index,notification_data=notification_data)
        data = "Shipping Set"
        return Response(data,status=status.HTTP_200_OK)
    
class shippedClass:
    @api_view(['GET'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getManifest(request,number):
        data = {}
        manifest = ShippingManifest.objects.select_related('warehouser','product').get(number=number)
        warehouse = Warehouse.objects.select_related('warehouser').prefetch_related('warehoused_products','processed_products').get(warehouser=request.user)
        warehouse.warehoused_products.add(manifest.product)
        warehouse.save()
        manifest.delete()
        data = f"{manifest.product} has been added to your inventory."
        return Response(data,status=status.HTTP_200_OK)
        




        

    
       

        