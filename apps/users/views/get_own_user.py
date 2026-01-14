from rest_framework import generics
from apps.users.serializers.read import UserSerializer
from permissions import IsOwner


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
