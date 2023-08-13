from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import DependingSerializers

# Create your views here.
class Depending:
    @api_view(['POST'])
    def farmer_registration_view(request):
    
        serializer = DependingSerializers(data=request.data)
        data = {}
        if request.user:
            if serializer.is_valid():
                account = serializer.save()  
                data['response'] = f"{account.username} depending account created"
                return Response(data,status = status.HTTP_201_CREATED)
            else:
                data = serializer.errors
                print(serializer.errors)
                return Response(data,status=status.HTTP_400_BAD_REQUEST)
        else:
            data['response'] = f"No admin for new user"
            return Response(data,status = status.HTTP_400_BAD_REQUEST) 