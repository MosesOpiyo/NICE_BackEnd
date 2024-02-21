from rest_framework import serializers
from .models import Payments
from Orders.serializers import OrderSerializers


class PaymentSerializers(serializers.ModelSerializer):
    order = OrderSerializers(read_only=True)
    class Meta:
        model = Payments
        fields = '__all__'

