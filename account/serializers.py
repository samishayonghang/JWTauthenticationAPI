from rest_framework import serializers
from account.models import User
from xml.dom import ValidationErr
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from.utils import Util
import os
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model=User
        fields=['email','name','password','password2','tc']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("password and confirm password doesnot match")
        return attrs
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    

class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','name']


class UserChangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True),
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True),
    class Meta:
        fields=['password','password2']
    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("password and confirm password doesnot match")
        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
   
    def validate(self,attrs):
        email=attrs.get('email')
        print('EMAIL_USER:', os.environ.get('EMAIL_USER'))
        print('EMAIL_PASS:', os.environ.get('EMAIL_PASS'))
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print('encoded UID',uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print('password reset token',token)
            link='http://localhost:3000/api/user/reset/'+uid+ '/' +token
            print('passoword reset link',link)
            #send email
            body='Click following link to reset your password'+link
            data= {
                'subject':'Reset your password',
                'body':body,
                'to_email':user.email
                
            }
            Util.send_email(data)
           
            return attrs

        else:
         raise ValidationErr ('you are not a registered user')
        

class UserPasswordResetSerializer(serializers.Serializer):
  try:
        password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True),
        password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True),
   
        class Meta:
            fields=['password','password2']
        def validate(self,attrs):
            password=attrs.get('password')
            password2=attrs.get('password2')
        
            uid= self.context.get('uid')
            token= self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("password and confirm password doesnot match")
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError('Token is not valid or expired')
            
            user.set_password(password)
            user.save()
            return attrs

      


  except DjangoUnicodeDecodeError as identifier:
       PasswordResetTokenGenerator().check_token(user ,token)
       raise ValidationError('Token is not valid or expired')