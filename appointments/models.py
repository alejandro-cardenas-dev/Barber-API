from django.db import models

from barbers.models import Barber
from customers.models import Customer

class Appointment(models.Model):
  barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  appointment_date = models.DateField()
  appointment_start_time = models.CharField(max_length=5)

  class Meta:
    unique_together = ('barber', 'appointment_date', 'appointment_start_time')

  def __str__(self):
    return f'Appointment to : {self.customer.name} with {self.barber.name} barber'