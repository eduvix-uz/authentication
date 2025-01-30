from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import UserLoginSerializer
from rabbitmq_messages.producers.UserLogin_producer import user_login
import asyncio
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# Login
class UserLoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            refresh = RefreshToken.for_user(user)
            async def login_user(username, user_id, is_staff, email, first_name, last_name):
                await user_login(username, user_id, is_staff, email, first_name, last_name)

            asyncio.run(login_user(user.username, user.id, user.is_staff, user.email, user.first_name, user.last_name))
            
            photo_url = f"{request.scheme}://{request.get_host()}{user.photo.url}" if user.photo else None
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'id': user.id,
                'is_staff': user.is_staff,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'photo': photo_url
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
