from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer
from rest_framework import status
# Create your views here.
class UserRegistrationView(APIView):
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()


            return Response({'msg':'Registration success'},status=status.HTTP_201_CREATED)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
    