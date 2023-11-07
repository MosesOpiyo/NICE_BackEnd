from rest_framework import serializers
from Authentication.serializers import UserSerializer
from .models import Requests

class RequestsSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Requests
        fields = '__all__'