from rest_framework import generics
from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer, CreateAppointmentSerializer
from barbers.models import Barber
from customers.models import Customer
from permissions import IsBarber, IsCustomer, IsOwner
from rest_framework.permissions import AllowAny

# Create Appointment
class CreateAppointment(generics.CreateAPIView):
  serializer_class = CreateAppointmentSerializer
  permission_classes = [IsCustomer]


# Delete Appointment
class DeleteAppointment(generics.DestroyAPIView):
  queryset = Appointment.objects.all()
  serializer_class = AppointmentSerializer
  permission_classes = [IsOwner]


# Get Appointment For Customer-Owner
class GetCustomerAppointment(generics.ListAPIView):
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
  serializer_class = AppointmentSerializer
  permission_classes = [IsBarber]

  def get_queryset(self):
    barber = Barber.objects.get(user__email=self.request.user)

    if not barber:
      return Appointment.objects.none()

    return Appointment.objects.filter(barber=barber)