from datetime import datetime, timedelta, time
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

class Barber(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  work_start_time = models.TimeField(default=time(10, 0), blank=False, null=False)
  work_end_time = models.TimeField(default=time(16, 0), blank=False, null=False)
  lunch_start_time = models.TimeField(default=time(12, 0))
  lunch_end_time = models.TimeField(default=time(14, 0))

  @staticmethod
  def validate_schedule_values(work_start_time, work_end_time, lunch_start_time, lunch_end_time):
    if work_start_time >= work_end_time:
      raise ValidationError('Work start time must be earlier than finish time.')

    if lunch_start_time >= lunch_end_time:
      raise ValidationError('Lunch start time must be earlier than finish time.')

    if not (work_start_time < lunch_start_time < work_end_time):
      raise ValidationError({'lunch_start_time': 'Lunch start time must be during working hours.'})

    if not (work_start_time < lunch_end_time < work_end_time):
      raise ValidationError({'lunch_end_time': 'Lunch end time must be during working hours.'})

  def clean(self):
    self.validate_schedule_values(
      self.work_start_time,
      self.work_end_time,
      self.lunch_start_time,
      self.lunch_end_time
    )
    super().clean()

  def save(self, *args, **kwargs):
    self.full_clean()
    super().save(*args, **kwargs)


  # Feat: change name get_available_times -> get_barber_work_times
  def get_available_times(self, interval=30):
    times = []
    rest_times = []

    current = datetime.combine(datetime.today(), self.work_start_time)
    end = datetime.combine(datetime.today(), self.work_end_time)
    lunch_start = datetime.combine(datetime.today(), self.lunch_start_time)
    lunch_end = datetime.combine(datetime.today(), self.lunch_end_time)


    while lunch_start < lunch_end:
      rest_times.append(lunch_start)
      lunch_start += timedelta(minutes=interval)

    while current < end:
      if current in rest_times:
        current += timedelta(minutes=interval)
        continue

      times.append(current.strftime('%H:%M'))
      current += timedelta(minutes=interval)

    return times

  def __str__(self):
    return f'Barber: {self.user.first_name} {self.user.last_name}'