from datetime import date
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from apps.appointments.models import Appointment
from apps.barbers.service.availability import calculate_barber_availability_for_date


def create_appointment(*, barber, customer, service, appointment_date, appointment_start_time):
  today = date.today()

  if appointment_date < today:
    raise ValidationError({
      'appointment_date': 'You cannot schedule an appointment for a past date.'
    })

  try:
    available_times = calculate_barber_availability_for_date(
      barber=barber,
      selected_date=appointment_date
    )
  except ValueError as e:
    raise ValidationError({'appointment_date': str(e)})

  appointment_start_str = appointment_start_time.strftime('%H:%M')
  if appointment_start_str not in available_times:
    raise ValidationError({
      'appointment_start_time': 'Time not available for this barber.'
    })

  try:
    appointment = Appointment.objects.create(
      barber=barber,
      customer=customer,
      service=service,
      appointment_date= appointment_date,
      appointment_start_time=appointment_start_time
    )
    return appointment
  except IntegrityError:
    raise ValidationError({
      'appointment_start_time': 'This time slot is already booked.'
    })