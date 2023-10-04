from rest_framework import serializers
from .models import Cart,Order
from Authentication.serializers import UserSerializer
from Farming.serializers import ProductsSerializers
from Warehouser.serializers import WarehouseSerializers

class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class OrderSerializers(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    product = ProductsSerializers(read_only=True)
    warehouse = WarehouseSerializers(read_only=True)
    class Meta:
        model = Order
        fields = "__all__"

