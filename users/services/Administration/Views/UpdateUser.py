from users.models import User
from users.serializers import UserUpdateSerializer
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

# Update user by admin
class UserManageViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAdminUser]