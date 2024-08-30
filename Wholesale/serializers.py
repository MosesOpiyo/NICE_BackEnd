from rest_framework import serializers

from Authentication.models import Account

from models import WholesaleEnterprise

class GetWholeSaleSerailzers(serializers.ModelSerializer):
    class Meta:
        model = WholesaleEnterprise
        fields = "__all__"

class WholesaleSerializers(serializers.ModelSerializer):
    class Meta:
        model = WholesaleEnterprise
        fields = ['business_name','type_of_business','shipping_address','business_status','duration_of_operation','date_to_start_receiving_coffee_orders','more_about_the_business']

    def save(self,request):
        user = Account.objects.get(id=request.user.id)
        wholesale = WholesaleEnterprise(
            user = user,
            business_name = self.validated_data['business_name'],
            type_of_business = self.validated_data['type_of_business'],
            shipping_address = self.validated_data['shipping_address'],
            business_status = self.validated_data['business_status'],
            duration_of_operation = self.validated_data['duration_of_operation'],
            date_to_start_receiving_coffee_orders = self.validated_data['date_to_start_receiving_coffee_orders'],
            more_about_the_business = self.validated_data['more_about_the_business']
        )
        wholesale.save()
        return wholesale

    