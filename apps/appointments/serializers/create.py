from rest_framework import serializers
from apps.appointments.models import Appointment

class CreateAppointmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Appointment
    fields = ['id', 'barber', 'created_at', 'appointment_date', 'appointment_start_time']

  def create(self, validated_data):
    from apps.appointments.services.creation import create_appointment
    from django.core.exceptions import ValidationError as DjangoValidationError

    customer = self.context['customer']
    validated_data['appointment_start_time'] = validated_data['appointment_start_time'].strftime('%H:%M')

    try:
      create_appointment(
        customer=customer,
        **validated_data
      )
      return validated_data

    except DjangoValidationError as e:
      raise serializers.ValidationError(e.message_dict)