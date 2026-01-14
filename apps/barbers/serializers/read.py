from rest_framework import serializers
from apps.barbers.models import Barber
from apps.users.serializers.read import UserSerializer

class BarberSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  barber_working_hours = serializers.SerializerMethodField()
  class Meta:
    model = Barber
    fields = ['id', 'user', 'work_start_time', 'work_end_time', 'lunch_start_time', 'lunch_end_time', 'barber_working_hours']

  def get_barber_working_hours(self, obj):
    return obj.generate_working_time_slots()
