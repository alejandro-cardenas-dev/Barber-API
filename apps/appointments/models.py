from django.core.exceptions import ValidationError
from datetime import date, datetime
from django.db import models
from apps.barbers.models import Barber
from apps.customers.models import Customer

class Appointment(models.Model):
  barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  appointment_date = models.DateField()
  appointment_start_time = models.TimeField()

  class Meta:
    unique_together = ('barber', 'appointment_date', 'appointment_start_time')

  def clean(self):
    today = date.today()
    now = datetime.now()

    if self.appointment_date < today:
      raise ValidationError({
        'appointment_date': 'You cannot schedule an appointment for a past date.'
      })

    if self.appointment_date == today and self.appointment_start_time <= now:
      raise ValidationError({
        'appointment_start_time': 'You cannot schedule an appointment for a past time.'
      })

    return super().clean()

  def __str__(self):
    return (
      f"{self.appointment_date} {self.appointment_start_time} - "
      f"{self.customer.user.first_name} with {self.barber.user.first_name}"
    )