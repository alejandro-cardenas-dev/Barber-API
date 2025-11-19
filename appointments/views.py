from rest_framework import generics
from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer, CreateAppointmentSerializer
from customers.models import Customer
from permissions import IsCustomer, IsOwner
from rest_framework.permissions import IsAuthenticated

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

  def perform_create(self, serializer):
    instance = Customer.objects.get(user=self.request.user)
    serializer.save(customer=instance)

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