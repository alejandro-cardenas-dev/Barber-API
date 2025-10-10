from django.contrib.auth.models import User
from django.db import models

class Customer (models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
  last_name = models.CharField(blank=True, max_length=250)
  phone_number = models.IntegerField(blank=True)

  def __str__(self):
    return f'Customer: {self.user.username} {self.last_name}'