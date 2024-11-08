from rest_framework import serializers

from Authentication.models import Account

from .models import WholesaleEnterprise

class GetWholeSaleSerailzers(serializers.ModelSerializer):
    class Meta:
        model = WholesaleEnterprise
        fields = "__all__"

class WholesaleSerializers(serializers.ModelSerializer):
    class Meta:
        model = WholesaleEnterprise
        fields = ['full_names','business_name','email','phone_number','type_of_business','shipping_address','business_status','more_about_the_business']

    def save(self,request):
        user = Account.objects.get(id=request.user.id)
        wholesale = WholesaleEnterprise(
            full_names = self.validated_data['full_names'],
            business_name = self.validated_data['business_name'],
            email = self.validated_data['email'],
            phone_number = self.validated_data['phone_number'],
            type_of_business = self.validated_data['type_of_business'],
            shipping_address = self.validated_data['shipping_address'],
            business_status = self.validated_data['business_status'],
            more_about_the_business = self.validated_data['more_about_the_business']
        )
        wholesale.user = user
        wholesale.save()
        user.is_wholesaler = True
        user.save()
        return wholesale
    

class NewWholesaleSerializers(serializers.ModelSerializer):
    class Meta:
        model = WholesaleEnterprise
        fields = ['full_names','business_name','email','phone_number','type_of_business','shipping_address','business_status','date_to_start_operating','more_about_the_business']

    def save(self,request):
        user = Account.objects.get(id=request.user.id)
        wholesale = WholesaleEnterprise(
            full_names = self.validated_data['full_names'],
            business_name = self.validated_data['business_name'],
            email = self.validated_data['email'],
            phone_number = self.validated_data['phone_number'],
            type_of_business = self.validated_data['type_of_business'],
            shipping_address = self.validated_data['shipping_address'],
            business_status = self.validated_data['business_status'],
            date_to_start_operating = self.validated_data['date_to_start_operating'],
        
            more_about_the_business = self.validated_data['more_about_the_business']
        )
        wholesale.user = user
        wholesale.save()
        user.is_wholesaler = True
        user.save()
        return wholesale
    


    