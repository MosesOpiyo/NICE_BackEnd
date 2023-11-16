from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.contrib.auth import authenticate
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status

from Farming.models import FarmerProfile
from Orders.models import Cart
from .serializers import *
from .models import *
from .tokens import create_jwt_pair_for_user
    
@api_view(['POST'])
def registration_view(request):
    
    serializer = BuyerRegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        new_cart = Cart.objects.create(
            buyer = account
        )
        new_cart.save()
        data['response'] = f"Successfully created a buyer under {account.username} with email {account.email}"
        return Response(data,status = status.HTTP_201_CREATED)
    else:
        error = serializer.errors.pop('email')
        data = f"{error[0]}"
        print(error[0])
        return Response(data,status=status.HTTP_400_BAD_REQUEST)
   
    
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
    
@api_view(['POST'])
def origin_warehouser_registration_view(request): 
    serializer = OriginWarehouserRegistrationSerializer(data=request.data)
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
    
@api_view(['POST'])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(email=email, password=password)

    if user is not None:

        tokens = create_jwt_pair_for_user(user)

        response = {"tokens": tokens}
        content = {"user": str(request.user), "auth": str(request.auth)}
        return Response(data=response, status=status.HTTP_200_OK)

    else:
        return Response(data={"message": "Invalid email or password"})
    

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
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


