from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.serializers import UserLoginSerializer
from rabbitmq_messages.producers.UserLogin_producer import user_login
import asyncio

# Login
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            asyncio.run(user_login(username=serializer.validated_data['username'], user_id=serializer.validated_data['id']))
            print(f'User: {serializer.validated_data["username"]}, id: {serializer.validated_data["id"]} logged in')
            return Response({"detail": "Login successful.", "data": serializer.validated_data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
