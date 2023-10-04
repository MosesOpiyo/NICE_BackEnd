import binascii,os
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import Pending_Account

class PendingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pending_Account
        fields = ['email','farmer_registration_number','username','phone_number']
        

    def save(self):
        user = Pending_Account(email=self.validated_data['email'],
                               username = self.validated_data['username'],
                               index=binascii.hexlify(os.urandom(5)).decode('utf-8'),
                               phone_number = self.validated_data['phone_number'],
                               farmer_registration_number = self.validated_data['farmer_registration_number'])
        user.save()
        return user
    
        
class GetPendingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pending_Account
        fields = ['id','index','email','username','phone_number','farmer_registration_number']
        extra_kwargs = {
            'password':{'write_only':True}
        }