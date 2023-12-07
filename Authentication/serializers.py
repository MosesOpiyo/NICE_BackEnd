from rest_framework import serializers
from .models import *
import binascii,os
from random import randint
from Notifications.serialiazers import GetNotificationsSerializers
from .email import send_welcome_email
from Orders.models import Cart
from django.contrib.auth import authenticate
from .tokens import create_jwt_pair_for_user

class AdminRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['email','password','username','index']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

    def save(self):
        user = Admin(email=self.validated_data['email'],username = self.validated_data['username'],index=AdminRegistrationSerializer.random_with_N_digits(10))
        user.index = binascii.hexlify(os.urandom(5)).decode('utf-8')
        user.set_password(self.validated_data['password'])
        user.save()
        return user
    
class FarmerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email','password','username','index']
        extra_kwargs = {
            'password':{'write_only':True},
        }
    
    def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

    def save(self):
        user = Farmer(email=self.validated_data['email'],username = self.validated_data['username'],index=FarmerRegistrationSerializer.random_with_N_digits(10))
        user.index = binascii.hexlify(os.urandom(5)).decode('utf-8')
        user.set_password(self.validated_data['password'])
        user.save()
        code = VerificationCode.objects.create(
           user = user 
        )
        code.code = FarmerRegistrationSerializer.random_with_N_digits(5)
        code.save()
        send_welcome_email(name=user.username,receiver=user.email,code=code.code)
        return user
    
class OriginWarehouserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OriginWarehouser
        fields = ['email','password','username']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

    def save(self):
        user = OriginWarehouser(email=self.validated_data['email'],username = self.validated_data['username'],index=OriginWarehouserRegistrationSerializer.random_with_N_digits(10))
        user.index = binascii.hexlify(os.urandom(5)).decode('utf-8')
        user.set_password(self.validated_data['password'])
        user.save()
        return user
    
class WarehouserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouser
        fields = ['email','password','username']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

    def save(self):
        user = Warehouser(email=self.validated_data['email'],username = self.validated_data['username'],index=WarehouserRegistrationSerializer.random_with_N_digits(10))
        user.index = binascii.hexlify(os.urandom(5)).decode('utf-8')
        user.set_password(self.validated_data['password'])
        user.save()
        return user
    
class BuyerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ['email','password','username']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        user = Buyer(email=self.validated_data['email'],username = self.validated_data['username'])
        user.index = binascii.hexlify(os.urandom(5)).decode('utf-8')
        user.set_password(self.validated_data['password'])
        user.save()
        new_cart = Cart.objects.create(
            buyer = user
        )
        new_cart.save()
        new_user = authenticate(email=self.validated_data['email'], password=self.validated_data['password'])
        tokens = create_jwt_pair_for_user(new_user)
        response = {"tokens": tokens}
        return response
    

class UserSerializer(serializers.ModelSerializer):
    notifications = GetNotificationsSerializers(many=True)
    class Meta:
        model = Account
        fields = ['email','username','type','notifications']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['index','email','username','type','date_joined','last_login']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'

class ProfilePicSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'
