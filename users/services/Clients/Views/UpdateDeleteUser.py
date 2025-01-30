from rest_framework import permissions
from users.models import User
from users.serializers import UserUpdateSerializer
from users.permissions import IsOwner
from rest_framework.generics import RetrieveUpdateDestroyAPIView


# Update and delete profile by user
class UserUpdateProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    
    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj