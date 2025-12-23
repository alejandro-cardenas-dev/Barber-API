from rest_framework import generics
from apps.appointments.models import Appointment
from apps.appointments.serializers.read import AppointmentSerializer
from permissions import IsOwner

# Delete Appointment
class DeleteAppointment(generics.DestroyAPIView):
  """
    Delete an existing appointment.

    Only the owner of the appointment can delete it (barber or customer).

    **Response:**
    - 204: Appointment successfully deleted
    - 404: Appointment not found
  """
  queryset = Appointment.objects.all()
  serializer_class = AppointmentSerializer
  permission_classes = [IsOwner]