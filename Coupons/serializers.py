from rest_framework import serializers
from .models import Coupon
from Authentication.models import Account

class CouponSerializers(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"

    def save(self,request):
        coupon = Coupon(
            name = self.validated_data['name'],
            discount = self.validated_data['discount']
        )
        coupon.save()
        buyers = Account.objects.filter(type = "BUYER")
        for buyer in buyers:
            buyer.coupons.add(coupon)
        return coupon 
    
class GetCouponSerializers(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"

