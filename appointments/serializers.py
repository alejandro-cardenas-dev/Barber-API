from rest_framework import serializers
from datetime import date
from appointments.models import Appointment
from barbers.models import Barber
from barbers.serializers import SimpleBarberSerializer
from customers.serializers import CustomerSerializer


class CreateAppointmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Appointment
    fields = ['id', 'barber', 'customer', 'created_at', 'appointment_date', 'appointment_start_time']

  def validate_appointment_date(self, value):
    today = date.today()

    if value < today:
        raise serializers.ValidationError('You cannot schedule an appointment for a date earlier than today.')

    return value

  def validate_appointment_start_time(self, value):
    barber_id = self.initial_data.get('barber')

    if not barber_id:
      raise serializers.ValidationError('You must specify a barber.')

    try:
      barber = Barber.objects.get(id=barber_id)
    except Barber.DoesNotExist:
      raise serializers.ValidationError('Barber does not exist.')

    available_times = barber.get_available_times()

    if value not in available_times:
      raise serializers.ValidationError('Time not available for this barber.')

    return value


class AppointmentSerializer(serializers.ModelSerializer):
  barber = SimpleBarberSerializer(read_only=True)
  customer = CustomerSerializer(read_only=True)

  class Meta:
    model = Appointment
    fields = ['id', 'barber', 'customer', 'created_at', 'appointment_date', 'appointment_start_time']