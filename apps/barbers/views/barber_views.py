from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.appointments.serializers.appointment_serializers import BarberDetailSerializer
from apps.barbers.models import Barber
from apps.barbers.serializers.barber_serializers import BarberSerializer, EditBarberScheduleSerializer
from apps.barbers.services.barber_services import calculate_barber_availability_for_date
from permissions import IsAdmin, IsBarber


class BarberListView(generics.ListAPIView):
  """
  Retrieve a list of all barbers.
  Accessible by anyone.

  **Response:**
  - 200: List of barbers with their basic information.
  """
  queryset = Barber.objects.all()
  serializer_class = BarberSerializer
  permission_classes = [AllowAny]


class BarberAvailabilityByDateView(APIView):
  """
  Get available working hours for a specific barber on a given date.
  Accessible by anyone.

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
  permission_classes = [AllowAny]

  def get(self, request, barber_id):
    barber = get_object_or_404(Barber, id=barber_id)

    date_str = request.query_params.get('date')
    if not date_str:
      raise ValidationError({'error': 'Missing date parameter. Example: ?date=2025-10-20'})

    try:
      selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
      raise ValidationError({'error': 'Invalid date format. Use YYYY-MM-DD.'})

    try:
      available_times = calculate_barber_availability_for_date(
        barber=barber,
        selected_date=selected_date
      )
    except ValueError as e:
      raise ValidationError({'error': str(e)})

    return Response({
      'barber_id': barber.id,
      'barber': barber.user.first_name,
      'date': date_str,
      'available_times': available_times
    })


class BarberScheduleListUpdateView(generics.RetrieveUpdateAPIView):
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
    try:
      return Barber.objects.get(user=self.request.user)
    except Barber.DoesNotExist:
      raise NotFound('No barber has been found for this user.')


class BarberDetailAdminView(generics.RetrieveAPIView):
  """
  Retrieve full barber details including appointments.
  Only accessible by admin.
  """
  queryset = Barber.objects.all()
  serializer_class = BarberDetailSerializer
  permission_classes = [IsAdmin]