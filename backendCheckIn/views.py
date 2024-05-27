from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer
from django.contrib.auth.models import User
from users.models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import authentication_classes
from django.utils import timezone
import requests
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import uuid
from rest_framework.views import APIView

# @api_view(['POST'])
# def login(req):
#     user = get_object_or_404(CustomUser, username=req.data['username'])
#     if not user.check_password(req.data['password']):
#         return Response({'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)
#     token = Token.objects.get_or_create(user=user)
#     serializer = UserSerializer(instance=user)
#     return Response({'token': token[0].key ,"user": serializer.data})

@api_view(['POST'])
def login(req):
    # user = get_object_or_404(CustomUser, username=req.data['username'])

    try:
        user = CustomUser.objects.get(username=req.data['username'])
    except ObjectDoesNotExist:
        return Response({'error': 'Username not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if not user.check_password(req.data['password']):
        return Response({'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not user.is_activated:
        return Response({'error': 'User account is not activate'}, status=status.HTTP_403_FORBIDDEN)

    if user.is_logged_in:
        return Response({'error': 'User is already logged in'}, status=status.HTTP_409_CONFLICT)

    # Fetch current time from World Time API
    world_time_response = requests.get('https://worldtimeapi.org/api/ip')
    if world_time_response.status_code == 200:
        current_time = world_time_response.json()['datetime']
        user.last_login = current_time
    else:
        # Fallback to Django's timezone.now() if World Time API call fails
        user.last_login = timezone.now()
        
    user.is_logged_in = True
    user.save()
    
    token = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({'token': token[0].key, 'user': serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register(req):
    serializer = UserSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        user = CustomUser.objects.get(username=req.data['username'])
        user.set_password(req.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def token(req):
    serializer = UserSerializer(req.user)
    return Response({"user": serializer.data.username })

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def logout(req):
    req.user.is_logged_in = False
    req.user.save()
    req.user.auth_token.delete()
        
    return Response({'message': 'Logged out successfully'})
