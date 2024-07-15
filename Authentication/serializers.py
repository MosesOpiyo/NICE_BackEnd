import random
import string
import binascii,os
from random import randint
from rest_framework import serializers

from .models import *

from random import randint
from Notifications.serialiazers import GetNotificationsSerializers
from Coupons.serializers import GetCouponSerializers
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
        fields = ['email','password','phone_number','username','index']
        extra_kwargs = {
            'password':{'write_only':True},
        }
    
    def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

    def save(self):
        user = Farmer(email=self.validated_data['email'],username = self.validated_data['username'],phone_number = self.validated_data['phone_number'],index=FarmerRegistrationSerializer.random_with_N_digits(10))
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
    session = serializers.CharField(max_length=100)
    class Meta:
        model = Buyer
        fields = ['email','password','username','session']
        extra_kwargs = {
            'password':{'write_only':True},
            'session':{'write_only':True},
            
        }

    def save(self):
        user = Buyer(email=self.validated_data['email'],username = self.validated_data['username'])
        user.index = binascii.hexlify(os.urandom(5)).decode('utf-8')
        user.set_password(self.validated_data['password'])
        user.save()
        coupon = Coupon.objects.get(name="First Time Purchase")
        user.coupons.add(coupon)
        try:
            user_cart = Cart.objects.get(
            session_id = self.validated_data['session']
            )
        except:
            user_cart = Cart.objects.create(
            session_id = self.validated_data['session']
            )
        user_cart.buyer = user
        user_cart.save
        new_user = authenticate(email=self.validated_data['email'], password=self.validated_data['password'])
        tokens = create_jwt_pair_for_user(new_user)
        response = {"tokens": tokens}
        return {
            "user":user,
            "response":response
        }
    
class RegistrationByAdminSerializer(serializers.ModelSerializer):
    account_type = serializers.CharField(write_only=True)
    class Meta:
        model = Account
        fields = ['email','phone_number','username','account_type']

    def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

    def save(self):
        print(self.validated_data)
        if self.validated_data['account_type'] == "ORIGINWAREHOUSER":
            user = OriginWarehouser(email=self.validated_data['email'],username = self.validated_data['username'],index=WarehouserRegistrationSerializer.random_with_N_digits(10))
            user.index = binascii.hexlify(os.urandom(5)).decode('utf-8')
            password = RegistrationByAdminSerializer.generate_strong_password()
            print(password)
            user.set_password(password)
            user.save()
        elif self.validated_data['account_type'] == "WAREHOUSER":
            user = Warehouser(email=self.validated_data['email'],username = self.validated_data['username'],index=WarehouserRegistrationSerializer.random_with_N_digits(10))
            user.index = binascii.hexlify(os.urandom(5)).decode('utf-8')
            password = RegistrationByAdminSerializer.generate_strong_password()
            print(password)
            user.set_password(password)
            user.save()
        elif self.validated_data['account_type'] == "ADMIN":
            user = Admin(email=self.validated_data['email'],username = self.validated_data['username'],index=WarehouserRegistrationSerializer.random_with_N_digits(10))
            user.index = binascii.hexlify(os.urandom(5)).decode('utf-8')
            password = RegistrationByAdminSerializer.generate_strong_password()
            print(password)
            user.set_password(password)
            user.save()
        return user
    
    def generate_strong_password():
        length = 12
        # Define character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special_characters = string.punctuation
        
        # Ensure the password has at least one character from each set
        all_characters = [random.choice(lowercase), random.choice(uppercase), random.choice(digits), random.choice(special_characters)]
        
        # Fill the remaining length of the password
        remaining_length = length - 4
        all_characters += random.choices(lowercase + uppercase + digits + special_characters, k=remaining_length)
        
        # Shuffle the characters to avoid predictable sequences
        random.shuffle(all_characters)
        
        # Join the list into a string and return
        password = ''.join(all_characters)
        return password
    

class UserSerializer(serializers.ModelSerializer):
    coupons = GetCouponSerializers(many=True)
    notifications = GetNotificationsSerializers(many=True)
    class Meta:
        model = Account
        fields = ['email','username','phone_number','type','purchases','coupons','notifications']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['index','email','phone_number','username','type','date_joined','last_login']

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

class PasswordRecoverySerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255)
    pass_token = serializers.CharField(max_length=255)
