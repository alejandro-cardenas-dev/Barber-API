from django.conf import settings
from django.db import models

class Customer (models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )

  def __str__(self):
    return f'Customer: {self.user.first_name} {self.user.last_name}'