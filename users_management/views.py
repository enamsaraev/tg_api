from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404

from dbcore.models import User
from users_management.serializers import BaseUserSerializer, BaseUserLoginSerializer


class UserRegistration(APIView):
    """User registration"""

    permission_classes = [AllowAny,]

    def post(self, request):
        ser = BaseUserSerializer(data=request.data) 
        ser.is_valid(raise_exception=True)
        ser.save()

        return Response(ser.data) 


class UserLogin(APIView):
    """User login"""
    permission_classes = [AllowAny,]

    def post(self, request):
        ser = BaseUserLoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        user = authenticate(request, email=ser.data['email'], password=ser.data['password'])
        if not user:
            raise APIException('Invalid credentials!')    
        
        login(request, user)
        return Response({'login': True})
    

class UserLogOut(APIView):
    """USer logout"""

    def get(self, request):
        logout(request)
        return Response({'logout': True})


class GetUserInfo(APIView):
    """Get usual info about user"""

    def get(self, request):
        user = get_object_or_404(User, id=request.data['id'])
        ser = BaseUserSerializer(user)

        return Response(ser.data)