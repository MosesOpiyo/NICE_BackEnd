from rest_framework import serializers
from .models import Cart,Order,CartItem,Sample
from Authentication.serializers import UserSerializer
from Farming.models import ProcessedProducts
from Farming.serializers import GetProductsSerializers,GetProcessedProductsSerializers
from Warehouser.serializers import WarehouseSerializers
from Notifications.models import Notification

from Authentication.models import Account
from Warehouser.models import Warehouse

class UpdateCartItemsSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['weight','quantity','grind','roast_type','price','code','subscription',"type"]

class SampleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = ['weight','quantity','price']

    def save(self,id):
        product = ProcessedProducts.objects.get(id=id)
        sample = Sample(
            weight = self.validated_data['weight'],
            quantity = self.validated_data['quantity'],
            price = self.validated_data['price']
        )
        sample.product = product
        sample.save()
        return sample

class GetSampleSerializer(serializers.ModelSerializer):
    product = GetProcessedProductsSerializers(read_only=True)
    class Meta:
        model = Sample
        fields = "__all__"



class CartItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['weight','quantity','grind','roast_type','price','code','subscription','frequency',"type"]

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
            subscription=self.validated_data['subscription'],
            frequency=self.validated_data['frequency']
            )
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
            weight = self.validated_data['weight'],
            grind = "None",
            roast_type = "None",
            price = self.validated_data['price'],
            code = self.validated_data['code'],
            type = "Green",
            subscription=self.validated_data['subscription'],
            frequency=self.validated_data['frequency']
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
    samples = GetSampleSerializer(many=True)
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

    def create_order(self, user):
        cart = Cart.objects.get(buyer=user)
        for item in cart.products:
            warehouse = Warehouse.objects.get(processed_products = item)
            if warehouse:
                order = Order(
                    buyer = user,
                    product = cart.products,
                    warehouse = warehouse,
                    is_paid = True
                )
                order.save()
                return order


    


