from rest_framework import serializers

from barbers.models import Barber

class BarberSerializer(serializers.ModelSerializer):
  class Meta:
    model = Barber
    fields = ['id', 'name', 'last_name', 'phone_number']