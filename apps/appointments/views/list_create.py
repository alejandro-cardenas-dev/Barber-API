from rest_framework import generics
from apps.appointments.models import Appointment
from apps.appointments.serializers.create import CreateAppointmentSerializer
from apps.appointments.serializers.read import AppointmentSerializer
from apps.customers.models import Customer
from permissions import IsCustomer


class AppointmentListCreateView(generics.ListCreateAPIView):
  """
    List or create appointments.

    **GET:** List all appointments for the authenticated user.
    **POST:** Create a new appointment (customers only).
  """

  def get_serializer_class(self):
    if self.request.method == 'POST':
      return CreateAppointmentSerializer
    return AppointmentSerializer

  def get_queryset(self):
    user = self.request.user

    if user.is_barber:
      return Appointment.objects.filter(barber=user.barber)

    if user.is_customer:
      return Appointment.objects.filter(customer=user.customer)

    return Appointment.objects.none() #chek this out

  def get_serializer_context(self): #check this out
    context = super().get_serializer_context()

    if self.request.method == 'POST' and self.request.user.is_customer:
      context['customer'] = Customer.objects.get(user=self.request.user)

    return context

  def get_permissions(self):
    if self.request.method == 'POST':
      return [IsCustomer()]
    return super().get_permissions()