from rest_framework.exceptions import ValidationError
from datetime import date, datetime
from apps.appointments.models import Appointment

def calculate_barber_availability_for_date (barber, selected_date):
  today = date.today()
  now = datetime.now().strftime('%H:%M')

  if selected_date < today:
    raise ValidationError({
      'error': 'You cannot see schedules for previous dates.'
    })

  booked_times = set(Appointment.objects.filter(
    barber=barber,
    appointment_date=selected_date
  ).values_list('appointment_start_time', flat=True))

  booked_times = [times.strftime('%H:%M') for times in booked_times]

  working_hours = barber.generate_working_time_slots()

  available_times = []

  for time_slot in working_hours:
    if time_slot in booked_times:
      continue
    if selected_date == today and time_slot <= now :
      continue

    available_times.append(time_slot)
  return available_times