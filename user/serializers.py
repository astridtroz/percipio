from rest_framework import serializers
from user.models import MyUser, Contributor, Provider
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from user.utils import Util
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model=MyUser
        fields=['email', 'name', 'user_type', 'password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password!=password2:
            raise serializers.ValidationError("Password and confirm password do not match")
        return attrs
    
    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=MyUser
        fields=['email','password']

class ContributorProfileSerializer(serializers.ModelSerializer): 
    email = serializers.EmailField(source='user_obj.email')
    name = serializers.CharField(source='user_obj.name')
    user_type = serializers.CharField(source='user_obj.user_type')

    class Meta:
        model = Contributor
        fields = ['id', 'email', 'user_type', 'name']

class ProviderProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user_obj.email')
    name = serializers.CharField(source='user_obj.name')
    user_type = serializers.CharField(source='user_obj.user_type')

    class Meta:
        model = Provider
        fields = ['id', 'email', 'user_type', 'name']


class ChangePasswordSerializer(serializers.Serializer):
    password= serializers.CharField(max_length=255,style={'input_type':'password'}, write_only=True)
    password2= serializers.CharField(max_length=255,style={'input_type':'password'}, write_only=True)
    class Meta:
        fields=['password','password2']
    
    def validate(self, attrs):
        password= attrs.get('password')
        password2= attrs.get('password2')
        user= self.context.get('user')
        if password!=password2:
            raise serializers.ValidationError("Password and confirm password do not match")
        
        user.set_password(password2)
        user.save()

        return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email= serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    
    def validate(self , attrs):
        email=attrs.get('email')
        if MyUser.objects.filter(email=email).exists:
            user=MyUser.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            link='http://localhost:8000/api/user/reset-password/'+uid+'/'+token+'/'
            print(link)
            body='Click following link to reset your password : '+ link
            data={
                'subject':'Reset your password',
                'body':body,
                'to_email': user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise ValidationError('You are not a registered user')

class UserPasswordResetSerializer(serializers.Serializer):
    password= serializers.CharField(max_length=255,style={'input_type':'password'}, write_only=True)
    password2= serializers.CharField(max_length=255,style={'input_type':'password'}, write_only=True)
    class Meta:
        fields=['password','password2']
    
    def validate(self, attrs):
        try:
            password= attrs.get('password')
            password2= attrs.get('password2')
            user= self.context.get('user')
            uid= self.context.get('uid')
            token=self.context.get('token')
            if password!=password2:
                raise serializers.ValidationError("Password and confirm password do not match")
            
            id =smart_str(urlsafe_base64_decode(uid))
            user=MyUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError('Token is invalid or expired')
            
            user.set_password(password2)
            user.save()

            return attrs
        except DjangoUnicodeDecodeError as Identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError('Token is invalid or expired')

