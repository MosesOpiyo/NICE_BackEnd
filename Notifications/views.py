import datetime
import binascii,os
from decouple import config
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from firebase_admin import db
from .serialiazers import GetNotificationsSerializers

class Notifications:
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def send_notification_to_user(user_index, notification_data):
      data = {}
      notification_info = {
          'id':binascii.hexlify(os.urandom(5)).decode('utf-8'),
          'recepient':user_index,
          'title':notification_data['title'],
          'body':notification_data['body'],
          'time':f'{datetime.datetime.now()}',
          'seen': False
      }
      ref = db.reference('/')
      reference = ref.child('Notifications')
      reference.push().set(
        notification_info
      )
      data = "Successfully sent"
      return Response(data,status=status.HTTP_200_OK)
    
    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def getNotifications(request):
        notifications = []
        ref = db.reference('/')
        notifications = ref.child('Notifications').order_by_child("recepient").equal_to(f"{request.user.index}").get()
        return Response(data=notifications,status=status.HTTP_200_OK)
    
