from rest_framework.throttling import AnonRateThrottle
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
  permission_classes = [AllowAny]
  throttle_classes = [AnonRateThrottle]