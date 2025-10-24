from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from barbers.models import Barber
from users.serializers import UserSerializer


class BarberSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  available_times = serializers.SerializerMethodField()

  class Meta:
    model = Barber
    fields = ['id', 'user', 'work_start_time', 'work_end_time', 'lunch_start_time', 'lunch_end_time', 'available_times']

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
    fields = ['work_start_time', 'work_end_time', 'lunch_start_time', 'lunch_end_time']

  def validate(self, data):
    instance = getattr(self, 'instance', None)

    work_start = data.get('work_start_time', getattr(instance, 'work_start_time', None))
    work_end = data.get('work_end_time', getattr(instance, 'work_end_time', None))
    lunch_start = data.get('lunch_start_time', getattr(instance, 'lunch_start_time', None))
    lunch_end = data.get('lunch_end_time', getattr(instance, 'lunch_end_time', None))

    try:
      Barber.validate_schedule_values(work_start, work_end, lunch_start, lunch_end)
    except DjangoValidationError as error:
      raise serializers.ValidationError({'deatil': error.messages})

    return data