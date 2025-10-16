from rest_framework import generics
from users.serializers import CreateUserSerializer
from rest_framework.permissions import AllowAny

class CreateUserView(generics.CreateAPIView):
  serializer_class = CreateUserSerializer
  permission_classes = [AllowAny]