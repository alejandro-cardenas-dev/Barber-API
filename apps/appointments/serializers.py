from rest_framework import serializers
from apps.appointments.models import Appointment
from apps.barbers.serializers import SimpleBarberSerializer
from apps.customers.serializers import CustomerSerializer


class CreateAppointmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Appointment
    fields = ['id', 'barber', 'created_at', 'appointment_date', 'appointment_start_time']

  def create(self, validated_data):
    from apps.appointments.services.creation import create_appointment
    from django.core.exceptions import ValidationError as DjangoValidationError

    customer = self.context['customer']

    try:
      create_appointment(
        customer=customer,
        **validated_data
      )

    except DjangoValidationError as e:
      raise serializers.ValidationError(e.message_dict)

class AppointmentSerializer(serializers.ModelSerializer):
  barber = SimpleBarberSerializer(read_only=True)
  customer = CustomerSerializer(read_only=True)

  class Meta:
    model = Appointment
    fields = ['id', 'barber', 'customer', 'created_at', 'appointment_date', 'appointment_start_time']