from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

from .serializers import OptionSerailzers

# Create your views here.
class Pricing:
    @api_view(["POST"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def new_price(request,id):
        data = {}
        serializer = OptionSerailzers(data=request.data)
        if serializer.is_valid():
            serializer.save(id=id)
            data = "New Price added"
            return Response(data=data,status=status.HTTP_201_CREATED)
        else:
            data = serializer.error_messages
            return Response(data=data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)