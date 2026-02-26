import re

from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import serializers

from apps.users.models import User
from apps.users.services.user_registration import register_user


class CreateUserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, required=True)
  password2 = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = User
    fields = [
      'id', 'first_name', 'last_name', 'email', 'phone',
      'password', 'password2', 'is_barber', 'is_customer'
    ]

  def validate_password(self, value):
    try:
      django_validate_password(value)
    except DjangoValidationError as e:
      raise serializers.ValidationError(e.messages)
    return value

  def validate_phone(self, value):
    if not re.fullmatch(r'\d{10}', value):
        raise serializers.ValidationError("Phone must contain exactly 10 digits.")
    return value

  def validate_first_name(self, value):
    if len(value) < 3:
      raise serializers.ValidationError("Name must have 3 or more characters")
    return value

  def validate_last_name(self, value):
    if len(value) < 3:
      raise serializers.ValidationError("Last name must have 3 or more characters"  )
    return value

  def validate(self, attrs):
    attrs = super().validate(attrs)

    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError(
        {"password": "Password do not match."}
      )
    if attrs.get('is_barber') == attrs.get('is_customer'):
      raise serializers.ValidationError(
        {"role": "User must be either a barber or a customer, not both or neither."}
      )

    return attrs

  def create(self, validated_data):
    password = validated_data.pop('password')
    validated_data.pop('password2')

    return register_user(
      password=password,
      **validated_data
    )