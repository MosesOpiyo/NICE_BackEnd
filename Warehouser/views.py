from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Warehouse
from Farming.models import CoffeeProducts
from .serializers import WarehouseSerializers,GetWarehouseSerializers,GetWarehouseProductsSerializers
from Farming.serializers import ProductsSerializers

class WarehouseClass:
    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def createWareHouse(request):
        data = {}
        serializer = WarehouseSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = "New warehouse created"
            return Response(data,status=status.HTTP_201_CREATED)
        
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_warehouse(request):
        data = {}
        warehouse = Warehouse.objects.select_related('warehouser').prefetch_related('warehoused_products').get(warehouser=request.user)
        data =  GetWarehouseSerializers(warehouse).data
        return Response(data,status = status.HTTP_200_OK)
    
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_warehouse_products(request):
        data = {}
        products = CoffeeProducts.objects.select_related('producer').all()
        data =  ProductsSerializers(products,many=True).data
        return Response(data,status = status.HTTP_200_OK)
       

        