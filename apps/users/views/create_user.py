from rest_framework import generics
from rest_framework.permissions import AllowAny
from apps.users.serializers.create import CreateUserSerializer


# Create Users
class UserCreateView(generics.CreateAPIView):
  """
    Register a new user.

    Anyone can create a new user account.

    **Request body:**
    - email (string): User's email (required)
    - password (string): User's password (required)
    - first_name (string): User's first name (required)
    - last_name (string): User's last name (required)

    **Response:**
    - 201: User successfully created
    - 400: Validation error (e.g., email already exists, password too short)
  """
  serializer_class = CreateUserSerializer
  permission_classes = [AllowAny]