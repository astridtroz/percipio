from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserLoginSerializer

class RegistrationView(APIView):
    def post(self,request):
        serializer= UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            return Response({'msg':'registration successful'},status= status.HTTP_201_CREATED)
    
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self,request):
        serializer= UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email, password=password)
            if user is not None:
                return Response({'msg':'Login Successful'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    
