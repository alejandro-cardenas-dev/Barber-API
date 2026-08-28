from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

from apps.barbers.models import Barber
from apps.catalog.models import Service
from apps.customers.models import Customer


class AppointmentStatus(models.TextChoices):
  CONFIRMED = 'confirmed', 'Confirmed'
  CANCELLED = 'cancelled', 'Cancelled'
  COMPLETED = 'completed', 'Completed'

class Appointment(models.Model):
  barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='appointments')
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='appointments')
  service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
  created_at = models.DateTimeField(auto_now_add=True)
  appointment_date = models.DateField()
  appointment_start_time = models.TimeField()
  status = models.CharField(max_length=10, choices=AppointmentStatus.choices, default= AppointmentStatus.CONFIRMED)
  cancelled_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True, blank=True,
    related_name='cancelled_appointments'
  )

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

  @property
  def is_completed(self):
    appointment_dt = datetime.combine(self.appointment_date, self.appointment_start_time)
    appointment_end = appointment_dt + timedelta(minutes=30)
    return timezone.now() > timezone.make_aware(appointment_end)

  @classmethod
  def update_completed_appointments(cls):
    now = timezone.now()

    appointments = cls.objects.filter(status=AppointmentStatus.CONFIRMED)

    for appointment in appointments:
      appointment_dt = datetime.combine(appointment.appointment_date, appointment.appointment_start_time)

      appointment_end = appointment_dt + timedelta(minutes=30)

      appointment_end = timezone.make_aware(appointment_end, timezone.get_current_timezone())

      if now >= appointment_end:
        appointment.status = AppointmentStatus.COMPLETED
        appointment.save(update_fields=['status'])