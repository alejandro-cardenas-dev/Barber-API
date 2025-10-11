from rest_framework import serializers

from barbers.models import Barber
from users.serializers import UserSerializer

class BarberSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)

  class Meta:
    model = Barber
    fields = ['user']