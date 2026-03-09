from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle

from apps.users.serializers.user_serializers import CreateUserSerializer, UserSerializer
from permissions import IsAdmin


class UserCreateView(generics.CreateAPIView):
  """
  Register a new user.

  - Customers can self-register (AllowAny).
  - Only admin can create barber accounts.

  **Request body:**
  - email (string): User's email (required)
  - password (string): User's password (required)
  - password2 (string): Password confirmation (required)
  - first_name (string): User's first name (required)
  - last_name (string): User's last name (required)
  - phone (string): 10 digit phone number (required)
  - is_barber (boolean): True if registering as a barber (required)
  - is_customer (boolean): True if registering as a customer (required)

  **Response:**
  - 201: User successfully created
  - 400: Validation errors:
    - Email already registered
    - Passwords do not match
    - Password does not meet requirements
    - Phone must contain exactly 10 digits
    - User must be either a barber or a customer, not both or neither
  """
  serializer_class = CreateUserSerializer
  throttle_classes = [AnonRateThrottle]

  def get_permissions(self):
    if self.request.data.get('is_barber'):
      return [IsAdmin()]
    return [AllowAny()]


class UserDetailView(generics.RetrieveAPIView):
  """
  Retrieve the authenticated user's profile information.
  Accessible by any authenticated user.

  **Request:**
  - Method: GET
  - URL: /users/me/
  - Headers:
      - Authorization: Bearer <token>

  **Response:**
  - 200: Returns the authenticated user's data
  - 401: Unauthorized (if token is missing or invalid)
  """
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user