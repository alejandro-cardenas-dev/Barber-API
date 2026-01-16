from rest_framework import serializers
from apps.catalog.models import Service


class ServiceReadSerializer(serializers.ModelSerializer):
  class Meta:
    model = Service
    fields = (
      'id',
      'name',
      'description',
      'price',
      'is_active',
      'created_at',
      'updated_at',
    )