from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from apps.appointments.models import Appointment
from apps.appointments.services.creation import create_appointment

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