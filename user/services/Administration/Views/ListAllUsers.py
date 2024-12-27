from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from user.models import User
from user.serializers import UserUpdateSerializer
 
# List of users for admin
class UserInfoView(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request, *args, **kwargs):
        users = User.objects.filter(is_staff=False, is_superuser=False)
        serializer = UserUpdateSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
