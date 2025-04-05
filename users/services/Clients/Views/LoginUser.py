from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# Login
class UserLoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'id': user.id,
                'is_staff': user.is_staff,
                'role': user.role,
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
