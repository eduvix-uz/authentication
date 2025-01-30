from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import PasswordResetConfirmSerializer
from django.core.mail import send_mail

class PasswordResetConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
