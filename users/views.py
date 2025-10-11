from django.shortcuts import render
from rest_framework import generics

from users.serializers import CreateUserSerializer

class CreateUserView(generics.CreateAPIView):
  serializer_class = CreateUserSerializer