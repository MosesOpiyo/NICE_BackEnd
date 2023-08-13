from rest_framework import serializers
from .models import Admin,Farmer,Warehouser,Buyer,Account,Profile

class AdminRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['email','password','username']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        user = Admin(email=self.validated_data['email'],username = self.validated_data['username'])
        user.set_password(self.validated_data['password'])
        user.save()
        return user
    
class FarmerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ['email','password','username']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        user = Farmer(email=self.validated_data['email'],username = self.validated_data['username'])
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

    def save(self):
        user = Warehouser(email=self.validated_data['email'],username = self.validated_data['username'])
        user.set_password(self.validated_data['password'])
        user.save()
        return user
    
class BuyerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouser
        fields = ['email','password','username']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        user = Buyer(email=self.validated_data['email'],username = self.validated_data['username'])
        user.set_password(self.validated_data['password'])
        user.save()
        return user
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email','username','type']

class ProfileSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'