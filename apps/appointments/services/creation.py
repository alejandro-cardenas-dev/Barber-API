from datetime import date
from django.core.exceptions import ValidationError
from apps.appointments.models import Appointment
from apps.barbers.service.availability import calculate_barber_availability_for_date

def create_appointment(*, barber, customer, appointment_date, appointment_start_time):
  today = date.today()

  if appointment_date < today:
    raise ValidationError({
      'appointment_date': 'You cannot schedule an appointment for a past date.'
    })

  available_times = calculate_barber_availability_for_date(
    barber=barber,
    selected_date= appointment_date
  )

  if appointment_start_time not in available_times:
    raise ValidationError({
      'appointment_start_time': 'Time not available for this barber.'
    })

  try:
    Appointment.objects.create(
      barber=barber,
      customer=customer,
      appointment_date= appointment_date,
      appointment_start_time=appointment_start_time
    )
  except:
    raise ValidationError({
      'appointment_start_time': 'This time slot has just been booked.'
    })