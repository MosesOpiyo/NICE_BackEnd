from rest_framework import serializers
from .models import Warehouse,ShippingManifest
from Authentication.serializers import UserSerializer
from Farming.serializers import ProductsSerializers

class WarehouseSerializers(serializers.ModelSerializer):
    warehouser = UserSerializer(read_only=True)
    class Meta:
        model = Warehouse
        fields = ['warehouser','name','location']

    def save(self,request):
        warehouse = Warehouse(
            name = self.validated_data['name'],
            location = self.validated_data['location'],
            warehouser = request.user
        )
        warehouse.save()
        return warehouse
    
class GetWarehouseSerializers(serializers.ModelSerializer):
    warehouser = UserSerializer(read_only=True)
    warehoused_products = ProductsSerializers(many=True)
    class Meta:
        model = Warehouse
        fields = ['name','warehouser','warehoused_products','location']

class GetWarehouseProductsSerializers(serializers.ModelSerializer):
    warehoused_products = ProductsSerializers(many=True)
    class Meta:
        model = Warehouse
        fields = ['warehoused_products']

class ShippingManifestSerializers(serializers.ModelSerializer):
    warehouser = UserSerializer(read_only=True)
    product = ProductsSerializers(read_only=True)
    class Meta:
        model = ShippingManifest
        fields = '__all__'


