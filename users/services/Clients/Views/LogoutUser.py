from users.serializers import LogoutUserSerializer
from users.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class LogoutUser(APIView):
    def post(self, request):
        serializer = LogoutUserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.data['email'])
            user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)