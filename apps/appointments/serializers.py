from rest_framework import serializers
from datetime import date, datetime
from apps.appointments.models import Appointment
from apps.barbers.models import Barber
from apps.barbers.serializers import SimpleBarberSerializer
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
    today =  date.today()
    now = datetime.now().strftime('%H:%M')
    barber = attrs['barber']
    appointment_date = attrs['appointment_date']
    appointment_date_str = attrs['appointment_date'].strftime('%Y-%m-%d')
    appointment_start_time = attrs['appointment_start_time'].strftime('%H:%M')

    if not barber:
      raise serializers.ValidationError('You must specify a barber.')

    booked_appointments = Appointment.objects.filter(
      barber=barber,
      appointment_date=appointment_date_str
    ).values_list('appointment_start_time', flat=True)

    available_times = barber.get_barber_available_times(booked_appointments, today, now, appointment_date)

    # breakpoint()
    if appointment_start_time not in available_times:
      raise serializers.ValidationError('Time not available for this barber.')

    return attrs


class AppointmentSerializer(serializers.ModelSerializer):
  barber = SimpleBarberSerializer(read_only=True)
  customer = CustomerSerializer(read_only=True)

  class Meta:
    model = Appointment
    fields = ['id', 'barber', 'customer', 'created_at', 'appointment_date', 'appointment_start_time']