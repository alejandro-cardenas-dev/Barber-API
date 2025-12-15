from rest_framework import serializers
from datetime import date
from apps.appointments.models import Appointment
from apps.barbers.serializers import SimpleBarberSerializer
from apps.barbers.service.availability import calculate_barber_availability_for_date
from apps.customers.serializers import CustomerSerializer


class CreateAppointmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Appointment
    fields = ['id', 'barber', 'created_at', 'appointment_date', 'appointment_start_time']

  def validate_appointment_date(self, value):
    today = date.today()

    if value < today:
        raise serializers.ValidationError('You cannot schedule an appointment for a date earlier than today.')

    return value

  def validate(self, attrs):
    barber = attrs['barber']
    appointment_date = attrs['appointment_date']
    appointment_start_time = attrs['appointment_start_time'].strftime('%H:%M')

    if not barber:
      raise serializers.ValidationError('You must specify a barber.')

    available_times = calculate_barber_availability_for_date(barber=barber, selected_date=appointment_date)

    if appointment_start_time not in available_times:
      raise serializers.ValidationError('Time not available for this barber.')

    return attrs


class AppointmentSerializer(serializers.ModelSerializer):
  barber = SimpleBarberSerializer(read_only=True)
  customer = CustomerSerializer(read_only=True)

  class Meta:
    model = Appointment
    fields = ['id', 'barber', 'customer', 'created_at', 'appointment_date', 'appointment_start_time']