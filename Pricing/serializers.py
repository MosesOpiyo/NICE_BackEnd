from rest_framework import serializers
from .models import Option

from Farming.models import ProcessedProducts

class OptionSerailzers(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = "__all__"

    def save(self,id):
        product = ProcessedProducts.objects.get(id=id)
        option = Option(
           quantity = self.validated_data['quantity'],
           regular_price = self.validated_data['regular_price'],
           wholesale_price = self.validated_data['wholesale_price'],
        )
        product.pricing.add(option)
        option.save()
        product.save()
        
