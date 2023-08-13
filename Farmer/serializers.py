from rest_framework import serializers
from .models import CoffeeProducts,WarehousingRequest
from Authentication.models import Farmer
from Authentication.serializers import UserSerializer

class ProductsSerializers(serializers.ModelSerializer):
    producer = UserSerializer(read_only=True)
    class Meta:
        model = CoffeeProducts
        fields = '__all__'
    def save(self,request):
        product = CoffeeProducts(name=self.validated_data['name'],quantity=self.validated_data['quantity'],warehouse_approved=False,producer=request.user)


class RequestSerializers(serializers.Serializer):
    class Meta:
        model = WarehousingRequest
        fields = '__all__'
