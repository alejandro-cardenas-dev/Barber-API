from datetime import date
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from apps.appointments.models import Appointment, AppointmentStatus
from apps.barbers.services.barber_services import calculate_barber_availability_for_date


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


def filter_appointments(*, queryset, status=None, appointment_date=None):
  if status:
    if status not in AppointmentStatus.values:
      raise ValidationError({
        'status': (
          f'Invalid status. '
          f'Valid values are: {", ".join(AppointmentStatus.values)}.'
        )
      })

    queryset = queryset.filter(status=status)

  if appointment_date:
    try:
      parsed_date = date.fromisoformat(appointment_date)

    except ValueError:
      raise ValidationError({
        'date': 'Invalid date format. Use YYYY-MM-DD.'
      })

    queryset = queryset.filter(
      appointment_date=parsed_date
    )

  return queryset