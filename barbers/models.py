from django.conf import settings
from django.db import models

class Barber(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )

  def __str__(self):
    return f'Barber: {self.user.first_name} {self.user.last_name}'