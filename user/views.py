from rest_framework.views import APIView
from django.contrib.auth.models import Permission
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .models import Contributor, Provider
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserPasswordResetSerializer,UserLoginSerializer, SendPasswordResetEmailSerializer,ChangePasswordSerializer,ContributorProfileSerializer, ProviderProfileSerializer
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        serializer= UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            if user.user_type == 'contributor':
                Contributor.objects.create(user_obj=user)
            elif user.user_type=='provider':
                Provider.objects.create(user_obj=user)
            token=get_tokens_for_user(user=user)
            return Response({'token':token, 'msg':'registration successful'},status= status.HTTP_201_CREATED)
    
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        serializer= UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email, password=password)
            if user is not None:
                token=get_tokens_for_user(user=user)
                return Response({ 'token':token,'msg':'Login Successful'},status=status.HTTP_200_OK, )
            else:
                return Response({'errors':{'non_field_errors':['Email or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    

class ContributorProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_type!= 'contributor':
            return Response({'error': 'Only contributors allowed'}, status=403)
        contributor = Contributor.objects.get(user_obj=request.user)
        serializer = ContributorProfileSerializer(contributor)
        return Response(serializer.data)

class ProviderProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_type != 'provider':
            return Response({'error': 'Only providers allowed'}, status=403)
        provider=Provider.objects.get(user_obj=user)
        serializer = ProviderProfileSerializer(provider)
        return Response(serializer.data)

class UserChangePassword(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]

    def post(self , request):
        serializer= ChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid():
            return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmail(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request):
        serializer= SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password reset link sent'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, uid, token):
        serializer= UserPasswordResetSerializer(data=request.data, context={'uid':uid ,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password reset successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

