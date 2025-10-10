from django.shortcuts import render
from rest_framework import generics
from barbers.models import Barber
from barbers.serializers import BarberSerializer

# Get Barbers
class GetBarber(generics.ListAPIView):
  queryset = Barber.objects.all()
  serializer_class = BarberSerializer

# Create Barber
class CreateBarber(generics.CreateAPIView):
  serializer_class = BarberSerializer

