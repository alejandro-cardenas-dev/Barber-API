from rest_framework import generics
from barbers.models import Barber
from barbers.serializers import BarberSerializer
from permissions import IsCustomer

# Get Barbers
class GetBarber(generics.ListAPIView):
  queryset = Barber.objects.all()
  serializer_class = BarberSerializer
  permission_classes = [IsCustomer]