from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.appointments.models import Appointment
from apps.appointments.services.appointment_services import create_appointment
from apps.barbers.models import Barber
from apps.barbers.serializers.barber_serializers import SimpleBarberSerializer
from apps.customers.serializers.customer_serializers import CustomerSerializer
from apps.users.serializers.user_serializers import UserSerializer


class AppointmentSerializer(serializers.ModelSerializer):
  barber = SimpleBarberSerializer(read_only=True)
  customer = CustomerSerializer(read_only=True)
  is_completed = serializers.BooleanField(read_only=True)

  class Meta:
    model = Appointment
    fields = [
      'id', 'barber', 'customer', 'created_at',
      'appointment_date', 'appointment_start_time', 'status', 'is_completed'
    ]


class CreateAppointmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Appointment
    fields = ['id', 'barber', 'service', 'created_at', 'appointment_date', 'appointment_start_time']
    validators = [
      UniqueTogetherValidator(
        queryset=Appointment.objects.all(),
        fields=['barber', 'appointment_date', 'appointment_start_time'],
        message='This time slot is already booked.'
      )
    ]

  def create(self, validated_data):
    customer = self.context['customer']
    try:
      appointment = create_appointment(customer=customer, **validated_data)
      return appointment
    except DjangoValidationError as e:
      raise serializers.ValidationError(e.message_dict)


class CancelAppointmentSerializer(serializers.ModelSerializer):
  """
  Serializer used exclusively for cancelling an appointment.
  Sets status to 'cancelled' and records who cancelled it.
  """
  class Meta:
    model = Appointment
    fields = ['id', 'status', 'cancelled_by']
    read_only_fields = ['id', 'status', 'cancelled_by']


# Placed here (instead of barbers/serializers.py) to avoid circular imports.
# BarberDetailSerializer depends on AppointmentSerializer which depends on SimpleBarberSerializer.
class BarberDetailSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  appointments = AppointmentSerializer(many=True, read_only=True)

  class Meta:
    model = Barber
    fields = [
      'id', 'user', 'work_start_time', 'work_end_time',
      'lunch_start_time', 'lunch_end_time', 'last_update', 'appointments', 'is_active'
    ]