from rest_framework import serializers
from apps.users.serializers.user_serializers import UserSerializer
from apps.customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  class Meta:
    model = Customer
    fields = ['id', 'user']