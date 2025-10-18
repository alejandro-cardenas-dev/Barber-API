from rest_framework import generics
from rest_framework.exceptions import NotFound
from barbers.models import Barber
from barbers.serializers import BarberSerializer, EditBarberScheduleSerializer
from permissions import IsBarber, IsCustomer

# Get Barbers
class GetBarber(generics.ListAPIView):
  queryset = Barber.objects.all()
  serializer_class = BarberSerializer
  permission_classes = [IsCustomer]

# Edit Barber Schedule For Working
class EditBarberSchedule(generics.UpdateAPIView):
  queryset = Barber.objects.all()
  serializer_class = EditBarberScheduleSerializer
  permission_classes = [IsBarber]

  def get_object(self):
    user = self.request.user
    try:
      return Barber.objects.get(user=user)
    except Barber.DoesNotExist:
      raise NotFound('No barber has been found for this user.')