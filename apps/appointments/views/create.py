from rest_framework import generics
from apps.appointments.serializers.create import CreateAppointmentSerializer
from apps.customers.models import Customer
from permissions import IsCustomer

# Create Appointment
class CreateAppointment(generics.CreateAPIView):
  """
    Create a new appointment.

    Only customers can create an appointment with a barber.

    **Request body:**
    - customer (int): ID of the customer (inferred from auth)
    - barber (int): ID of the barber
    - date (date field): Date of the appointment
    - time (string): Time of the appointment (format HH:MM)

    **Response:**
    - 201: Appointment successfully created
  """
  serializer_class = CreateAppointmentSerializer
  permission_classes = [IsCustomer]

  def get_serializer_context(self):
    context = super().get_serializer_context()
    context['customer'] = Customer.objects.get(user=self.request.user)
    return context