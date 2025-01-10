from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Cart,Order,ProductOrder,OrderItem,CartItem,Sample, Delivery, Payment, Billing, Order
from Authentication.serializers import UserSerializer
from Farming.models import ProcessedProducts
from Farming.serializers import GetProcessedProductsSerializers
from Notifications.models import Notification
from django.db import transaction

from Authentication.models import Account

from Payment.utils import make_paypal_payment

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
        
class OrderItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['weight','quantity','grind','roast_type','price',"type"]

    def save(self,id):
        product = ProcessedProducts.objects.get(id=id)
        if self.validated_data['grind'] != "None" or self.validated_data['roast_type'] != "None":
            order_item = OrderItem(
            product=product,
            weight = self.validated_data['weight'],
            quantity = self.validated_data['quantity'],
            grind = self.validated_data['grind'],
            price = self.validated_data['price'],
            roast_type = self.validated_data['roast_type'],
            type = "Roasted",
            )
            order_item.save()
            notification = Notification.objects.create(
                message = f"{product.product.name} is being processed for purchase.",
                route = "orders"
            )
            product.product.producer.notifications.add(notification)

            return order_item
        elif self.validated_data['grind'] == "None" or self.validated_data['roast_type'] == "None":
            order_item = OrderItem(
            product=product,
            weight = self.validated_data['weight'],
            grind = "None",
            roast_type = "None",
            price = self.validated_data['price'],
            type = "Green",
            ) 
            order_item.save()
            notification = Notification.objects.create(
                message = f"{product.product.name} is being processed for purchase.",
                route = "orders"
            )
            product.product.producer.notifications.add(notification)
            return order_item


class GetCartItemSerializers(serializers.ModelSerializer):
    product = GetProcessedProductsSerializers(read_only=True)
    class Meta:
        model = CartItem
        fields = "__all__"

class GetOrderItemSerializers(serializers.ModelSerializer):
    product = GetProcessedProductsSerializers(read_only=True)
    class Meta:
        model = OrderItem
        fields = "__all__"

class CartSerializers(serializers.ModelSerializer):
    products = GetCartItemSerializers(many=True)
    wishlist = GetProcessedProductsSerializers(many=True)
    samples = GetSampleSerializer(many=True)
    buyer = UserSerializer(read_only=True)
    class Meta:
        model = Cart
        fields = "__all__"

class ProductOrderSerializers(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.all(), slug_field='model'
    )
    object_id = serializers.IntegerField()
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = ProductOrder
        fields = ['id', 'content_type', 'object_id', 'content_object']

    def get_content_object(self, obj):
        """
        Dynamically serialize the related object (CartItem or OrderItem).
        """
        if obj.content_type.model == 'orderitem':
            # If it's an OrderItem, serialize it with GetOrderItemSerializers
            return GetOrderItemSerializers(obj.content_object).data
        elif obj.content_type.model == 'cartitem':
            # Handle CartItem similarly if needed
            return GetCartItemSerializers(obj.content_object).data
        return None

    def validate(self, attrs):
        """
        Custom validation to ensure only ModelB or ModelC is allowed.
        """
        allowed_models = ['cartitem', 'orderitem']
        if attrs['content_type'].model not in allowed_models:
            raise serializers.ValidationError("Only CartItem or OrderItem are allowed.")
        return attrs
            


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['country','city','state','company_name','residence','postal_code','first_name','last_name', 'address', 'email', 'phone_number', 'delivery_speed']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        exclude_fields = ['card_last_4_digits']


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    delivery = DeliverySerializer()
    payment = PaymentSerializer()
    billing = BillingSerializer()

    class Meta:
        model = Order
        fields = ['delivery','payment','billing']
    
    def create_cart_items(self,id, validated_data):
        with transaction.atomic():
            """
            Custom create method to handle nested serializers.
            """
            delivery_data = validated_data.pop('delivery')
            payment_data = validated_data.pop('payment')
            billing_data = validated_data.pop('billing')

            user = Account.objects.get(id=id)
            cart = Cart.objects.get(buyer=user)
            delivery = Delivery.objects.create(**delivery_data)
            payment = Payment.objects.create(**payment_data)
            billing = Billing.objects.create(**billing_data)

            order = Order.objects.create(delivery=delivery,
                        payment=payment, 
                        billing=billing, 
                        buyer = user
                        )
            total = 0
            for product in cart.products.all():
                content_type = ContentType.objects.get_for_model(product)
                product_created = ProductOrder.objects.create(
                    content_type=content_type,
                    object_id=product.id,
                    content_object=content_type.get_object_for_this_type(id=product.id),
                    order = order
                )
                total += product.price
            order.total = total
            order.save()
            if order.payment.payment_method == "paypal":
                status,paypal_url = make_paypal_payment(order=order)
            return status,paypal_url

    def create_order_items(self, request, id, validated_data):
        """
        Custom create method to handle nested serializers.
        """
        delivery_data = validated_data.pop('delivery')
        payment_data = validated_data.pop('payment')
        billing_data = validated_data.pop('billing')
        product_data = validated_data.pop('product')

        product = ProcessedProducts.objects.get(id=id)
        buyer = Account.objects.get(id=request.user.id)

        delivery = Delivery.objects.create(**delivery_data)
        payment = Payment.objects.create(**payment_data)
        billing = Billing.objects.create(**billing_data)

        item = OrderItem.objects.create(
            weight=product_data['weight'],
            quantity=product_data['quantity'],
            price=product_data['price'],
            grind=product_data['grind'],
            roast_type=product_data['roast_type'],
            type=product_data['type'],
            product=product  # Directly assign product
        )

        product_type = ContentType.objects.get_for_model(item)
        product_created = ProductOrder.objects.create(
            content_type=product_type,
            object_id=item.id,
            content_object=product_type.get_object_for_this_type(id=item.id)
        )

        order = Order.objects.create(
            buyer=buyer,
            delivery=delivery,
            payment=payment,
            billing=billing
        )
        buyer = Account.objects.get(id = request.user.id)
        order.buyer = buyer
        order.items.add(product_created)
        order.total = item.price
        order.save()

        if order.payment.payment_method == "paypal":
           status,paypal_url = make_paypal_payment(order=order)
        return status,paypal_url
    
class GetOrderSerializers(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    items = serializers.SerializerMethodField()
    delivery = DeliverySerializer(read_only=True)
    payment = PaymentSerializer(read_only=True)
    billing = BillingSerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

    def get_items(self, obj):
        """
        Fetch and serialize related ProductOrder objects for this order.
        """
        print(obj)
        order = Order.objects.get(id=obj.id)
        related_items = ProductOrder.objects.filter(order=obj)
        print([related_items])
        return ProductOrderSerializers(related_items, many=True).data
    
    


    


