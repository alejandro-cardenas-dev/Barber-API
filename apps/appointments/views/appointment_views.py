from rest_framework import generics, status
from rest_framework.response import Response

from apps.appointments.models import Appointment
from apps.appointments.serializers.appointment_serializers import (
  AppointmentSerializer,
  CancelAppointmentSerializer,
  CreateAppointmentSerializer,
)
from apps.customers.models import Customer
from permissions import IsAdmin, IsAppointmentOwner, IsCustomer, IsCustomerOrBarber


class AppointmentListCreateView(generics.ListCreateAPIView):
  """
  List or create appointments.

  **GET:**
  - Admin: returns all appointments.
  - Barber: returns only their own appointments.
  - Customer: returns only their own appointments.

  **POST:**
  - Only customers can create appointments.
  """

  def get_serializer_class(self):
    if self.request.method == 'POST':
      return CreateAppointmentSerializer
    return AppointmentSerializer

  def get_queryset(self):
    user = self.request.user
    queryset = Appointment.objects.select_related('barber__user', 'customer__user', 'service')

    if user.is_staff:
      return queryset.all()
    if user.is_barber:
      return queryset.filter(barber=user.barber)
    if user.is_customer:
      return queryset.filter(customer=user.customer)
    return Appointment.objects.none()

  def get_serializer_context(self):
    context = super().get_serializer_context()
    if self.request.method == 'POST' and self.request.user.is_customer:
      context['customer'] = Customer.objects.get(user=self.request.user)
    return context

  def get_permissions(self):
    if self.request.method == 'POST':
        return [IsCustomer()]
    return super().get_permissions()


class CancelAppointmentView(generics.UpdateAPIView):
  """
  Cancel an existing appointment via PATCH.

  - Customers can only cancel their own appointments.
  - Admin can cancel any appointment.

  Sets status to 'cancelled' and records who cancelled it.
  """
  queryset = Appointment.objects.all()
  serializer_class = CancelAppointmentSerializer
  http_method_names = ['patch']

  def get_permissions(self):
    if self.request.user.is_staff:
      return [IsAdmin()]
    return [IsCustomer(), IsAppointmentOwner()]

  def patch(self, request, *args, **kwargs):
    appointment = self.get_object()

    if appointment.status == 'cancelled':
      return Response(
        {'detail': 'This appointment is already cancelled.'},
        status=status.HTTP_400_BAD_REQUEST
      )

    if appointment.status == 'completed' or appointment.is_completed:
      return Response(
        {'detail': 'Cannot cancel a completed appointment.'},
        status=status.HTTP_400_BAD_REQUEST
      )

    appointment.status = 'cancelled'
    appointment.cancelled_by = request.user
    appointment.save()

    return Response(AppointmentSerializer(appointment).data, status=status.HTTP_200_OK)


class AppointmentDeleteView(generics.DestroyAPIView):
  """
  Permanently delete an appointment.
  Only accessible by admin.

  **Response:**
  - 204: Appointment successfully deleted.
  - 403: Forbidden if not admin.
  - 404: Appointment not found.
  """
  queryset = Appointment.objects.all()
  permission_classes = [IsAdmin]