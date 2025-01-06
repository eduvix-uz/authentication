from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.serializers import UserLoginSerializer
from rabbitmq_messages.producers.UserLogin_producer import user_login
import asyncio
from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# Login
class UserLoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            refresh = RefreshToken.for_user(user)
            asyncio.run(user_login(username=serializer.validated_data['username'], user_id=serializer.validated_data['id'], is_staff=serializer.validated_data['is_staff'], email=serializer.validated_data['email'], first_name=serializer.validated_data['first_name'], last_name=serializer.validated_data['last_name']))
            print(f'User: {serializer.validated_data["username"]}, id: {serializer.validated_data["id"]}, admin: {serializer.validated_data["is_staff"]}, email: {serializer.validated_data["email"]}, first_name: {serializer.validated_data["first_name"]}, last_name: {serializer.validated_data["last_name"]} logged in')
            return Response({"data": serializer.validated_data,
                             "refresh": str(refresh), 
                             "access": str(refresh.access_token)}, 
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
