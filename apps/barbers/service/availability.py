from rest_framework.exceptions import ValidationError
from datetime import date, datetime
from apps.appointments.models import Appointment

def calculate_barber_availability_for_date(barber, selected_date):
  today = date.today()
  now = datetime.now().replace(second=0, microsecond=0).time()

  if selected_date < today:
    raise ValueError('You cannot see schedules for previous dates.')

  booked_times = {
    t.strftime('%H:%M')
    for t in Appointment.objects.filter(
      barber=barber,
      appointment_date=selected_date
    ).values_list('appointment_start_time', flat=True)
  }

  working_hours = barber.generate_working_time_slots()
  available_times = []

  for time_slot in working_hours:
    if time_slot in booked_times:
      continue

    slot_time = datetime.strptime(time_slot, '%H:%M').time()
    if selected_date == today and slot_time <= now :
      continue

    available_times.append(time_slot)

  return available_times