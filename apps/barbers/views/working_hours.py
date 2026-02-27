from rest_framework.views import APIView
from apps.barbers.models import Barber
from apps.barbers.service.availability import calculate_barber_availability_for_date
from permissions import IsCustomer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from datetime import datetime
from rest_framework.exceptions import ValidationError

# Get Barbers' Working Hours In Specifc Date
class BarberAvailabilityByDateView(APIView):
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