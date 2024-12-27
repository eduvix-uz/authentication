from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from user.models import User
from rest_framework.exceptions import ValidationError

# Delete user by admin
class UserDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise ValidationError("User not found.")
    
    def delete(self, request, pk, *args, **kwargs):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)