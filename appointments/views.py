from rest_framework import generics
from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer, CreateAppointmentSerializer
from barbers.models import Barber
from customers.models import Customer
from permissions import IsBarber, IsCustomer, IsOwner
from rest_framework.permissions import AllowAny

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


# Get Appointment For Customer-Owner
class GetCustomerAppointment(generics.ListAPIView):
  """
    Retrieve all appointments for the logged-in customer.

    **Response:**
    - 200: List of appointments
  """
  queryset = Appointment.objects.all()
  serializer_class = AppointmentSerializer
  permission_classes = [IsCustomer]

  def get_queryset(self):
    customer = Customer.objects.get(user__email=self.request.user)

    if not customer:
      return Appointment.objects.none()

    return Appointment.objects.filter(customer=customer)


# Get Appointments For Each Barber
class GetBarberAppointment(generics.ListAPIView):
  """
    Retrieve all appointments for the logged-in barber.

    **Response:**
    - 200: List of appointments
  """
  serializer_class = AppointmentSerializer
  permission_classes = [IsBarber]

  def get_queryset(self):
    barber = Barber.objects.get(user__email=self.request.user)

    if not barber:
      return Appointment.objects.none()

    return Appointment.objects.filter(barber=barber)