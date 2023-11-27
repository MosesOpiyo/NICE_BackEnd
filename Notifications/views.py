import datetime
import binascii,os
from decouple import config
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Notification
from .serialiazers import GetNotificationsSerializers

class Notifications:
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def create_notifications(message,user_index,origin,farmer):
       notification = Notification.objects.create(
          message = message,
       )
       notification.recipients.add(user_index,origin,farmer)
       notification.save()
       data = "Successfully sent"
       return Response(data,status=status.HTTP_200_OK)
    
    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def get_notifications(request):
       notifications = Notification.objects.filter()
       notifications
       if len(notifications) > 1:
         data = GetNotificationsSerializers(notifications,many=True).data
         return Response(data,status=status.HTTP_200_OK)
       elif len(notifications) == 1:
         data = GetNotificationsSerializers(notifications).data 
         return Response(data,status=status.HTTP_200_OK)
       else:
         data = "No Notifications" 
         return Response(data,status=status.HTTP_200_OK) 
    
    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def seen_notifications(message,user_index):
       notifications = Notification.objects.filter(
          recepient_index = user_index
       )
       for notification in notifications:
          if notification.seen != True:
            notification.seen = True
          else:
            None
       return Response(data="Seen",status=status.HTTP_200_OK)
    
