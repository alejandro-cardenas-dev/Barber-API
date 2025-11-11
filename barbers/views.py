from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from appointments.models import Appointment
from rest_framework import generics
from barbers.models import Barber
from barbers.serializers import BarberSerializer, EditBarberScheduleSerializer
from permissions import IsBarber, IsCustomer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from datetime import date, datetime
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from permissions import IsOwner

# Get Barbers
class GetBarber(generics.ListAPIView):
  """
    Retrieve a list of all barbers.

    Only accessible by customers.

    **Response:**
    - 200: List of barbers with their basic information.
  """
  queryset = Barber.objects.all()
  serializer_class = BarberSerializer
  permission_classes = [IsCustomer]


# Get Barbers' Working Hours In Specifc Date
class GetBarberAvailableTimesSpecificDate(APIView):
  """
    Get available working hours for a specific barber on a given date.

    Only accessible by customers.

    **URL Parameters:**
    - barber_id (int): ID of the barber.

    **Query Parameters:**
    - date (string, required): The date to check availability (format: YYYY-MM-DD).

    **Response:**
    - 200: Dictionary with barber name, date, and available times.
    - 400: Error if date parameter is missing or in wrong format.
    - 404: Barber not found.

    **Example Response:**
    {
        "barber": "John",
        "date": "2025-10-20",
        "available_times": ["09:00", "10:00", "11:00"]
    }
  """
  permission_classes = [IsCustomer]

  def get(self, request, barber_id):
    today =  date.today()
    now = datetime.now().strftime('%H:%M')

    barber = get_object_or_404(Barber, id=barber_id)
    date_str = request.query_params.get('date')


    if not date_str:
      raise ValidationError({'error': 'Missing date parameter. Example: ?date=2025-10-20'}, code=400)

    try:
      selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
      raise ValidationError({'error': 'Invalid date format. Use YYYY-MM-DD.'})

    if selected_date < today:
      raise ValidationError({'error': 'You cannot see schedules for previous dates.'})

    booked_appointments = Appointment.objects.filter(
      barber=barber,
      appointment_date=date_str
    ).values_list('appointment_start_time', flat=True)


    available_times = barber.get_barber_available_times(booked_appointments, today, now, selected_date)

    return Response({
      'barber': barber.user.first_name,
      'date': date_str,
      'available_times': available_times
    })


# Get and Update Barber Schedule
class BarberScheduleView(generics.RetrieveUpdateAPIView):
  """
    Retrieve or update the working schedule of the logged-in barber.

    **GET:** Returns the current working schedule.
    **PUT/PATCH:** Updates one or more schedule fields.

    Only accessible by barbers themselves.

    **Request Body (for PUT/PATCH):**
    - work_start_time (HH:MM)
    - work_end_time (HH:MM)
    - lunch_start_time (HH:MM)
    - lunch_end_time (HH:MM)

    **Response:**
    - 200: Schedule data (both GET and PUT).
    - 404: Barber not found.
  """
  serializer_class = EditBarberScheduleSerializer
  permission_classes = [IsBarber]

  def get_object(self):
    user = self.request.user
    try:
      return Barber.objects.get(user=user)
    except Barber.DoesNotExist:
      raise NotFound("No barber has been found for this user.")