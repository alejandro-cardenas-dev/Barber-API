from rest_framework import generics
from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer, CreateAppointmentSerializer
from barbers.models import Barber
from permissions import IsBarber, IsCustomer

# Create Appointment
class CreateAppointment(generics.CreateAPIView):
  serializer_class = CreateAppointmentSerializer
  permission_classes = [IsCustomer]

# Get Appointments For Each Barber
class GetAppointment(generics.ListAPIView):
  serializer_class = AppointmentSerializer
  permission_classes = [IsBarber]

  def get_queryset(self):
    barber = Barber.objects.get(user__email=self.request.user)

    if not barber:
      return Appointment.objects.none()

    return Appointment.objects.filter(barber=barber)