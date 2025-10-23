from datetime import datetime, timedelta, time
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

class Barber(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  time_to_start_working = models.TimeField(default=time(10, 0), blank=False, null=False)
  time_to_finish_working = models.TimeField(default=time(16, 0), blank=False, null=False)

  def clean(self):
    if self.time_to_start_working >= self.time_to_finish_working:
      raise ValidationError('Start time must be earlier than finish time.')
    return super().clean()

  # Feat: change name get_available_times -> get_barber_work_times
  def get_available_times(self, interval=30):
    times = []

    current = datetime.combine(datetime.today(), self.time_to_start_working)
    end = datetime.combine(datetime.today(), self.time_to_finish_working)

    while current < end:
      times.append(current.strftime('%H:%M'))
      current += timedelta(minutes=interval)

    return times

  def __str__(self):
    return f'Barber: {self.user.first_name} {self.user.last_name}'