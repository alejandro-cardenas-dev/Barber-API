from rest_framework import serializers
from users.models import User
from barbers.models import Barber
from customers.models import Customer


class CreateUserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  password2 = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = [
      'id', 'first_name', 'last_name', 'email', 'phone',
      'password', 'password2', 'is_barber', 'is_customer'
    ]

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

  def validate_password(self, value):
    if len(value) < 8:
      raise serializers.ValidationError(
        {"password": "Password must contain 8 or more characters"}
      )
    return value

  def validate_phone(self, value):
    if len(value) != 10:
      raise serializers.ValidationError(
        {"phone": "Phone must contain exactly 10 digits"}
      )
    return value

  def validate_first_name(self, value):
    if len(value) < 3:
      raise serializers.ValidationError(
        {"first_name": "Name must have 3 or more characters"}
      )
    return value

  def validate_last_name(self, value):
    if len(value) < 3:
      raise serializers.ValidationError(
        {"last_name": "Last name must have 3 or more characters"}
      )
    return value


  def create(self, validated_data):
    password = validated_data.pop('password')
    validated_data.pop('password2')

    is_barber = validated_data.pop('is_barber', False)
    is_customer = validated_data.pop('is_customer', False)

    user = User.objects.create_user(
      **validated_data,
      password=password,
      is_barber=is_barber,
      is_customer=is_customer
    )

    if user.is_barber:
      Barber.objects.create(user=user)
    elif user.is_customer:
      Customer.objects.create(user=user)

    return user


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'is_barber', 'is_customer']