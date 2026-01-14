from rest_framework import serializers
from apps.barbers.models import Barber
from apps.users.serializers.read import UserSerializer

class SimpleBarberSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)

  class Meta:
    model = Barber
    fields = ['id', 'user']