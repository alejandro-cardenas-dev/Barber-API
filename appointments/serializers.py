from rest_framework import serializers

from appointments.models import Appointment
from barbers.serializers import BarberSerializer
from customers.serializers import CustomerSerializer

class CreateAppointmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Appointment
    fields = ['id', 'barber', 'customer', 'created_at', 'date_start']

class AppointmentSerializer(serializers.ModelSerializer):
  barber = BarberSerializer(read_only=True)
  customer = CustomerSerializer(read_only=True)
  class Meta:
    model = Appointment
    fields = ['id', 'barber', 'customer', 'created_at', 'date_start']