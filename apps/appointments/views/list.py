from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.appointments.models import Appointment
from apps.appointments.serializers.read import AppointmentSerializer

# Get Appointments
class GetAppointment(generics.ListAPIView):
  """
    Get all appointments for the owner.

    **Response:**
    - 200: List of appointments
  """
  serializer_class = AppointmentSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    user = self.request.user

    if user.is_barber:
      instance = user.barber
      return Appointment.objects.filter(barber=instance)
    elif user.is_customer:
      instance = user.customer
      return Appointment.objects.filter(customer=instance).order_by('appointment_date', 'appointment_start_time')