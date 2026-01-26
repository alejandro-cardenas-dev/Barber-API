from rest_framework import generics
from apps.barbers.models import Barber
from apps.barbers.serializers.read import BarberSerializer
from permissions import IsCustomer

# Get Barbers
class BarberListView(generics.ListAPIView):
  """
    Retrieve a list of all barbers.

    Only accessible by customers.

    **Response:**
    - 200: List of barbers with their basic information.
  """
  queryset = Barber.objects.all()
  serializer_class = BarberSerializer
  permission_classes = [IsCustomer]