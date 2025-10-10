from django.shortcuts import render
from rest_framework import generics
from customers.models import Customer
from customers.serializers import CustomerSerializer

# Get Customers
class GetCustomers(generics.ListAPIView):
  queryset = Customer.objects.all()
  serializer_class = CustomerSerializer

# Create Customer
class CreateCustomer(generics.CreateAPIView):
  serializer_class = CustomerSerializer