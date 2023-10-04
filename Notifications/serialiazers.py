from rest_framework import serializers
from .models import Notification

class GetNotificationsSerializers(serializers.Serializer):
    class Meta:
        fields = '__all__'