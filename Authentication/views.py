from rest_framework.decorators import api_view,permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from .serializers import *
from .models import *
    
@api_view(['POST'])
def registration_view(request):
    
    serializer = BuyerRegistrationSerializer(data=request.data)
    data = {}
    if request.user:
        if serializer.is_valid():
            account = serializer.save()  
            data['response'] = f"Successfully created a buyer under {account.username} with email {account.email}"
            return Response(data,status = status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            print(serializer.errors)
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
    else:
        data['response'] = f"No admin for new user"
        return Response(data,status = status.HTTP_400_BAD_REQUEST) 
    
@api_view(['POST'])
def admin_registration_view(request):
    
    serializer = AdminRegistrationSerializer(data=request.data)
    data = {}
    if request.user:
        if serializer.is_valid():
            account = serializer.save()  
            data['response'] = f"Successfully created a admin under {account.username} with email {account.email}"
            return Response(data,status = status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            print(serializer.errors)
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
    else:
        data['response'] = f"No admin for new user"
        return Response(data,status = status.HTTP_400_BAD_REQUEST) 
    
@api_view(['POST'])
def farmer_registration_view(request):
    
    serializer = FarmerRegistrationSerializer(data=request.data)
    data = {}
    if request.user:
        if serializer.is_valid():
            account = serializer.save()  
            data['response'] = f"Successfully created a farmer under {account.username} with email {account.email}"
            return Response(data,status = status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            print(serializer.errors)
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
    else:
        data['response'] = f"No admin for new user"
        return Response(data,status = status.HTTP_400_BAD_REQUEST) 
    
@api_view(['POST'])
def warehouser_registration_view(request):
    
    serializer = WarehouserRegistrationSerializer(data=request.data)
    data = {}
    if request.user:
        if serializer.is_valid():
            account = serializer.save()  
            data['response'] = f"Successfully created a warehouser under {account.username} with email {account.email}"
            return Response(data,status = status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            print(serializer.errors)
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
    else:
        data['response'] = f"No admin for new user"
        return Response(data,status = status.HTTP_400_BAD_REQUEST) 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):

    data = {}
    if request.user:
        try:
            profile = Profile.objects.select_related('user').get(user=request.user)
            data =  ProfileSerializer(profile).data
            return Response(data,status = status.HTTP_200_OK)
        except:
            new_profile = Profile.objects.create(user=request.user)
            data =  ProfileSerializer(new_profile).data
            return Response(data,status = status.HTTP_200_OK)
        
    else:
        return Response(data,status = status.HTTP_404_NOT_FOUND)
