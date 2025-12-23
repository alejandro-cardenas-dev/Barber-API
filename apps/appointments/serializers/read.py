from rest_framework import serializers
from apps.appointments.models import Appointment
from apps.barbers.serializers import SimpleBarberSerializer
from apps.customers.serializers import CustomerSerializer

class AppointmentSerializer(serializers.ModelSerializer):
  barber = SimpleBarberSerializer(read_only=True)
  customer = CustomerSerializer(read_only=True)

  class Meta:
    model = Appointment
    fields = ['id', 'barber', 'customer', 'created_at', 'appointment_date', 'appointment_start_time']