from rest_framework import serializers

from barbers.models import Barber
from users.serializers import UserSerializer

class BarberSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  available_times = serializers.SerializerMethodField()

  class Meta:
    model = Barber
    fields = ['id', 'user', 'time_to_start_working', 'time_to_finish_working', 'available_times']

  def get_available_times(self, obj):
    return obj.get_available_times()


class EditBarberScheduleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Barber
    fields = ['time_to_start_working', 'time_to_finish_working']