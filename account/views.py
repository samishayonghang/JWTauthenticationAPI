from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from.models import User
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated 
# Create your views here.
#generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response ({'token':token, 'msg':'Registration successfull'},status=status.HTTP_201_CREATED)


            
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

         email=serializer.data.get('email')
         password=serializer.data.get('password')
         user=authenticate(email=email,password=password)
         if user is not None:
             token=get_tokens_for_user(user)

             return Response({'token':token ,'msg':'Login success'},status=status.HTTP_200_OK)
         else:
             return Response({'errors':{'non_field_errors':['Email of password is not valid']}},status=status.HTTP_404_NOT_FOUND)
         
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        
        return Response(serializer.data,status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password changed sucessfully'},status=status.HTTP_200_OK)

            
class SendPasswordResetEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password reset link send please check your email'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordResetView(APIView):
     renderer_classes=[UserRenderer]
     def post(self,request,uid,token,format=None):
         serializer=UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
         if serializer.is_valid(raise_exception=True):
             return Response({'msg':'password reset successfully'},status=status.HTTP_200_OK)

         
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    