from django.shortcuts import render
from rest_framework import generics
from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer, CreateAppointmentSerializer

# Create Appointment
class CreateAppointment(generics.CreateAPIView):
  serializer_class = CreateAppointmentSerializer

# Get Appointments
class GetAppointment(generics.ListAPIView):
  queryset = Appointment.objects.all()
  serializer_class = AppointmentSerializer