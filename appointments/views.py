from django.shortcuts import render
from rest_framework import generics
from appointments.serializers import AppointmentSerializer

# Create Customer
class CreateAppointment(generics.CreateAPIView):
  serializer_class = AppointmentSerializer