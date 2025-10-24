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


# Serializer to use in appointment serializer
class SimpleBarberSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)

  class Meta:
    model = Barber
    fields = ['id', 'user']


class EditBarberScheduleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Barber
    fields = ['time_to_start_working', 'time_to_finish_working']

  def validate(self, data):
    start = data.get('time_to_start_working')
    end = data.get('time_to_finish_working')

    if start >= end:
      raise serializers.ValidationError({'error': 'Start time cannot be greater than or equal to the end time.'})

    return data