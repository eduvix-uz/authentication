from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import RequestPasswordSerializer

class RequestPasswordResetView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RequestPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request)
            return Response({"detail": "Password reset email sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
