from rest_framework import serializers

from customers.models import Customer
from users.serializers import UserSerializer

class CustomerSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  class Meta:
    model = Customer
    fields = ['id', 'user']
