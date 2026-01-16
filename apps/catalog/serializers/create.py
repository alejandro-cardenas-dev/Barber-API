from rest_framework import serializers
from apps.catalog.models import Service


class ServiceCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Service
    fields = [
      'id',
      'name',
      'description',
      'price',
      'is_active',
      'created_at',
      'updated_at'
    ]

    read_only_fields = ('id', 'created_at', 'updated_at')

  def validate_price(self, value):
    if value <= 0:
        raise serializers.ValidationError("Price must be greater than zero.")
    return value