from django.core.exceptions import ValidationError
from datetime import date, datetime
from django.db import models
from apps.barbers.models import Barber
from apps.catalog.models import Service
from apps.customers.models import Customer

class Appointment(models.Model):
  barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  service = models.ForeignKey(Service, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  appointment_date = models.DateField()
  appointment_start_time = models.TimeField()

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['barber', 'appointment_date', 'appointment_start_time'],
        name='unique_barber_appointment_slot'
      )
    ]

  def __str__(self):
    return (
      f"{self.appointment_date} {self.appointment_start_time} - "
      f"{self.customer.user.first_name} with {self.barber.user.first_name}"
    )