from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.contrib.auth import authenticate
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from cloudinary.uploader import upload

from Farming.models import FarmerProfile
from .email import send_welcome_email

from .serializers import *
from .models import *
from .tokens import create_jwt_pair_for_user
    
@api_view(['POST'])
def registration_view(request):
    
    serializer = BuyerRegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data = account
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
            data = account
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
        account = Account.objects.get(id = user.id)
        if account.is_confirmed == True:
            tokens = create_jwt_pair_for_user(user)
            response = {"tokens": tokens}
            content = {"user": str(request.user), "auth": str(request.auth)}
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data="Account not Verified", status=status.HTTP_200_OK)

    else:
        return Response(data={"message": "Invalid email or password"})

@api_view(['POST'])
def google_signin(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(email=email, password=password)
    if user is not None:
        tokens = create_jwt_pair_for_user(user)
        response = {"tokens": tokens}
        content = {"user": str(request.user), "auth": str(request.auth)}
        return Response(data=response, status=status.HTTP_200_OK)
    else:
        serializer = BuyerRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            response = serializer.save()
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            error = serializer.errors
            print(error)
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        
    
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updateData(request,key):
    data_update = request.data.get(f"{key}")
    user = Account.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    serialized_data = serializer.data
    for attribute in serialized_data.keys():
        if attribute == key:
            serialized_data[key] = data_update

    updated_serializer = UserSerializer(user,data=serialized_data)
    if updated_serializer.is_valid():
        updated_serializer.save()
        return Response(data="Updated",status = status.HTTP_200_OK)
    else:
        data = updated_serializer.errors
        print(data)   
        return Response(data,status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updatePassword(request):
    email = request.user.email
    password = request.data.get("password")
    new_password = request.data.get("new_password")
    user = authenticate(email=email, password=password)
    if user is not None:
        account = Account.objects.get(id = user.id)
        account.password = None
        account.set_password(new_password)
        account.is_confirmed = True
        account.save()
        return Response(data="Password Updated", status=status.HTTP_200_OK)
    else:
        return Response(data="Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

    
@api_view(['POST'])
def Verification(request):
    email = request.data.get("email")
    code = request.data.get("code")
    user = Account.objects.get(email=email)
    if user is not None:
        auth_code = VerificationCode.objects.get(user=user)
        if auth_code.code == code:
           account = Account.objects.get(email=email)
           account.is_confirmed = True
           account.save()
           auth_code.delete()
           return Response(data="Account Verified",status=status.HTTP_200_OK)
        else:
           auth_code.delete()   
           return Response(data="One time code Expired",status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(data="User not Found",status=status.HTTP_404_NOT_FOUND)

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
    

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def profilePicture(request):
    data = {}
    image_file = request.data.get("image")
    compressed_image = compress_image(image_file=image_file)
    cloudinary_response = upload(compressed_image)
    cloudinary_url = cloudinary_response['url'].replace('http://res.cloudinary.com/dlzyg12i7/', '')
    user_profile = Profile.objects.get(user=request.user)
    user_profile.profile_pic = cloudinary_url
    user_profile.save()
    data = f"{user_profile.user.username}'s profile pic has been set."
    return Response(data,status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_notification(request):
    data = {}
    notifications = request.POST.getlist("notificationsList[]")
    user = Account.objects.get(id = request.user.id)
    for notification in notifications:
        get_notification = Notification.objects.get(id=int(notification))
        user.notifications.remove(get_notification)
        get_notification.delete()
    return Response(data="Deleted",status=status.HTTP_200_OK)
        

from PIL import Image
from io import BytesIO

def compress_image(image_file):
        img = Image.open(image_file)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
    
        img.thumbnail((600, 600))
        
        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        return buffer.getvalue()
