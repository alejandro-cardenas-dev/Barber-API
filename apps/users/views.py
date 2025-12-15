from rest_framework import generics
from permissions import IsOwner
from apps.users.serializers import CreateUserSerializer, UserSerializer
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


# Get Personal User
class GetUser(generics.RetrieveAPIView):
  """
    Retrieve the authenticated user's profile information.

    This endpoint allows an authenticated user to fetch their own data.

    **Permissions:**
    - Only accessible to the owner of the account (IsOwner).

    **Request:**
    - Method: GET
    - URL: /get-user/
    - Headers:
        - Authorization: Bearer <token>

    **Response:**
    - 200: Returns the authenticated user's data
      Example:
      {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe"
      }

    - 401: Unauthorized (if token is missing or invalid)
  """
  serializer_class = UserSerializer
  permission_classes = [IsOwner]

  def get_object(self):
    return self.request.user
