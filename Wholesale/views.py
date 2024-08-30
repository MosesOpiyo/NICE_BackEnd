import binascii,os
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import WholesaleEnterprise
from .serializers import GetWholeSaleSerailzers,WholesaleSerializers

class Wholesale:
    @api_view(["POST"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def new_whole_enterprise(request):
        data = {}
        serializers = WholesaleSerializers(data = request.data)
        if serializers.is_valid():
            enterprise = serializers.save()
            data = f"New Wholesale Enterprise, {enterprise.business_name} Created"
            return Response(data=data,status=status.HTTP_201_CREATED)
        else:
            data = serializers.error_messages
            return Response(data=data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @api_view(["GET"])
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def whole_enterprise(request):
        data = {}
        enterprise = WholesaleEnterprise.objects.get(user=request.user)
        data = GetWholeSaleSerailzers(enterprise).data
        return Response(data=data,status=status.HTTP_200_OK)

