from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer
from rest_framework import generics
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
class LoginAPIView(APIView):
    permission_classes = []  # cho phép truy cập công khai
    authentication_classes = []  # không require JWT để login

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            "access": serializer.validated_data["access"],
            "refresh": serializer.validated_data["refresh"],
            "user": serializer.validated_data["user"],
        }, status=status.HTTP_200_OK)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer