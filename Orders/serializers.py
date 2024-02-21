from rest_framework import serializers
from .models import Cart,Order,CartItem
from Authentication.serializers import UserSerializer
from Farming.models import ProcessedProducts
from Farming.serializers import GetProductsSerializers,GetProcessedProductsSerializers
from Warehouser.serializers import WarehouseSerializers
from Notifications.models import Notification

class CartItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['weight','quantity','grind','roast_type','price','code','subscription',"type"]

    def save(self,id):
        product = ProcessedProducts.objects.get(id=id)
        if self.validated_data['grind'] != "None" or self.validated_data['roast_type'] != "None":
            cart_item = CartItem(
            product=product,
            weight = self.validated_data['weight'],
            quantity = self.validated_data['quantity'],
            grind = self.validated_data['grind'],
            price = self.validated_data['price'],
            roast_type = self.validated_data['roast_type'],
            code = self.validated_data['code'],
            type = "Roasted",
            )
            if self.validated_data['subscription'] == 'true':
                cart_item.subscription = True
            else:
                cart_item.subscription = False
            cart_item.save()
            notification = Notification.objects.create(
                message = f"{product.product.name} is being processed for purchase.",
                route = "orders"
            )
            product.product.producer.notifications.add(notification)

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
            notification = Notification.objects.create(
                message = f"{product.product.name} is being processed for purchase.",
                route = "orders"
            )
            product.product.producer.notifications.add(notification)
            return cart_item

class GetCartItemSerializers(serializers.ModelSerializer):
    product = GetProcessedProductsSerializers(read_only=True)
    class Meta:
        model = CartItem
        fields = "__all__"

class CartSerializers(serializers.ModelSerializer):
    products = GetCartItemSerializers(many=True)
    wishlist = GetProcessedProductsSerializers(many=True)
    buyer = UserSerializer(read_only=True)
    class Meta:
        model = Cart
        fields = "__all__"


class OrderSerializers(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    product = GetCartItemSerializers(many=True)
    warehouse = WarehouseSerializers(read_only=True)
    class Meta:
        model = Order
        fields = "__all__"

    


