from rest_framework import generics
from users.serializers import CreateUserSerializer
from rest_framework.permissions import AllowAny

# Create Users
class CreateUserView(generics.CreateAPIView):
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