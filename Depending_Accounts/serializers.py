from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import Depending_Account

class DependingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Depending_Account
        fields = ['email','password','username']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        user = Depending_Account(email=self.validated_data['email'],username = self.validated_data['username'])
        user.password = make_password(self.validated_data['password'])
        user.save()
        return user
        