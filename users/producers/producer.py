from rest_framework import viewsets
from rest_framework import permissions
from ..models import User
from ..serializers import UserDetailSerializer

# Send user info to payment service
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)