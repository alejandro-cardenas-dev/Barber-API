from django.db import models

class Customer (models.Model):
  name = models.CharField(max_length=250)
  last_name = models.CharField(max_length=250)
  phone_number = models.IntegerField()

  def __str__(self):
    return f'Customer: {self.name} {self.last_name}'