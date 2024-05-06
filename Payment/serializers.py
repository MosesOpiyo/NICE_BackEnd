from rest_framework import serializers
from .models import Payments,Address,Receipt
from Orders.serializers import OrderSerializers

import datetime
class PaymentSerializers(serializers.ModelSerializer):
    order = OrderSerializers(read_only=True)
    class Meta:
        model = Payments
        fields = '__all__'

class AddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

    def save(self):
        address = Address(
          first_name = self.validated_data['first_name'],
          last_name = self.validated_data['last_name'],
          phone_number = self.validated_data['phone_number'],
          address = self.validated_data['address'],
          company_address = self.validated_data['company_address'],
          city = self.validated_data['city'],
          country = self.validated_data['country'],
          postal_code = self.validated_data['postal_code']  
        )
        address.save()
        return address
    
class ReceiptSerializers(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['amount','payment_option','shipping_option']

    def save(self):
        new_receipt = Receipt(
            amount = self.validated_data['amount'],
            payment_option = self.validated_data['payment_option'],
            shipping_option = self.validated_data['shipping_option'],
            creation_date=datetime.datetime.now()
        )
        new_receipt.save()
        return new_receipt

