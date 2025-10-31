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
    barber = get_object_or_404(Barber, id=barber_id)
    today = date.today()
    date_str = request.query_params.get('date')
    time = datetime.now()
    time_str = time.strftime('%H:%M')

    if not date_str:
      return Response({'error': 'Missing date parameter. Example: ?date=2025-10-20'}, status=400)

    try:
      selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
      return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

    if selected_date < today:
      return Response({'error': 'You cannot see schedules for previous dates.'})

    available_times = barber.get_barber_working_hours()

    appointments = Appointment.objects.filter(barber=barber, appointment_date=selected_date)
    booked_appointments = appointments.values_list('appointment_start_time', flat=True)

    available_times_for_date = []

    for times in available_times:
      if times in booked_appointments:
        continue
      if today == selected_date and time_str >= times:
        continue
      available_times_for_date.append(times)

    return Response({
      'barber': barber.user.first_name,
      'date': date_str,
      'available_times': available_times_for_date
    })


# Edit Barber Schedule For Working
class EditBarberSchedule(generics.UpdateAPIView):
  """
    Edit the working schedule of the logged-in barber.

    Only accessible by barbers themselves.

    **Request Body:**
    - start_time (time field, optional): Start of working hours (format HH:MM)
    - end_time (time field, optional): End of working hours (format HH:MM)
    - lunch_start (time field, optional): Start of lunch hours (format HH:MM)
    - lunch_end (time field, optional): End of lunch hours (format HH:MM)

    **Response:**
    - 200: Updated barber schedule.
    - 404: Barber not found for the logged-in user.
  """
  queryset = Barber.objects.all()
  serializer_class = EditBarberScheduleSerializer
  permission_classes = [IsBarber]

  def get_object(self):
    user = self.request.user
    try:
      return Barber.objects.get(user=user)
    except Barber.DoesNotExist:
      raise NotFound('No barber has been found for this user.')