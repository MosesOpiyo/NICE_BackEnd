from rest_framework import serializers
from random import randint
from .models import Warehouse,ShippingManifest
from Authentication.serializers import UserSerializer
from Authentication.models import Account
from Farming.serializers import ProductsSerializers
from Farming.models import CoffeeProducts
from Notifications.models import Notification

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
    
class ShippingManifestSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShippingManifest
        fields = ['number','product','quantity','warehouser']

    def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

    def save(self,id):
        product = CoffeeProducts.objects.get(id=id)
        manifest = ShippingManifest(
            number = ShippingManifestSerializers.random_with_N_digits(8),
            product = product,
            quantity = self.validated_data['quantity'],
            warehouser = self.validated_data['warehouser']
        )
        product_quantity = product.quantity
        product.quantity = product_quantity - self.validated_data['quantity']
        product.save()
        manifest.save()
        return manifest

class GetShippingManifestSerializers(serializers.ModelSerializer):
    product = ProductsSerializers(read_only=True)
    class Meta:
        model = ShippingManifest
        fields = '__all__'
    
class GetWarehouseSerializers(serializers.ModelSerializer):
    warehouser = UserSerializer(read_only=True)
    warehoused_products = GetShippingManifestSerializers(many=True)
    class Meta:
        model = Warehouse
        fields = ['name','warehouser','warehoused_products','location','warehouse_area_storage']

class GetWarehouseProductsSerializers(serializers.ModelSerializer):
    warehoused_products = GetShippingManifestSerializers(many=True)
    class Meta:
        model = Warehouse
        fields = ['warehoused_products']



