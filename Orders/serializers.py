from rest_framework import serializers
from .models import Cart,Order,CartItem
from Authentication.serializers import UserSerializer
from Farming.models import ProcessedProducts
from Farming.serializers import ProductsSerializers,GetProcessedProductsSerializers
from Warehouser.serializers import WarehouseSerializers

class CartItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity','grind','roast_type','price','code',"type"]

    def save(self,id):
        product = ProcessedProducts.objects.get(id=id)
        if self.validated_data['grind'] != "None" or self.validated_data['roast_type'] != "None":
            cart_item = CartItem(
            product=product,
            quantity = self.validated_data['quantity'],
            grind = self.validated_data['grind'],
            price = self.validated_data['price'],
            roast_type = self.validated_data['roast_type'],
            code = self.validated_data['code'],
            type = "Roasted"
            )
            cart_item.save()
            return cart_item
        elif self.validated_data['grind'] == "None" or self.validated_data['roast_type'] == "None":
            cart_item = CartItem(
            product=product,
            quantity = 100,
            grind = "None",
            roast_type = "None",
            code = self.validated_data['code'],
            type = "Green"
            ) 
            cart_item.save()
            return cart_item

class GetCartItemSerializers(serializers.ModelSerializer):
    product = GetProcessedProductsSerializers(read_only=True)
    class Meta:
        model = CartItem
        fields = "__all__"

class CartSerializers(serializers.ModelSerializer):
    products = GetCartItemSerializers(many=True)
    buyer = UserSerializer(read_only=True)
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

    


