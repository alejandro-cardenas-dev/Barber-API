from rest_framework import serializers

from appointments.models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Appointment
    fields = ['id', 'barber', 'customer', 'created_at', 'date_start']