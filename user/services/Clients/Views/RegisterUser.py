from user.serializers import RegisterUserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Register a new user
class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully. Please check your email to verify your account.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)