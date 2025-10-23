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
  queryset = Barber.objects.all()
  serializer_class = BarberSerializer
  permission_classes = [IsCustomer]


# Get Barbers' Working Hours In Specifc Date
class GetBarberAvailableTimesSpecificDate(APIView):
  permission_classes = [IsCustomer]

  def get(self, request, barber_id):
    barber = get_object_or_404(Barber, id=barber_id)
    today = date.today()
    date_str = request.query_params.get('date')

    if not date_str:
      return Response({'error': 'Missing date parameter. Example: ?date=2025-10-20'}, status=400)

    try:
      selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
      return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

    if selected_date < today:
      return Response({'error': 'You cannot see schedules for previous dates.'})

    available_times = barber.get_available_times()

    appointments = Appointment.objects.filter(barber=barber, appointment_date=selected_date)
    booked_appointments = appointments.values_list('appointment_start_time', flat=True)

    available_times_for_date = []

    for times in available_times:
      if times not in booked_appointments:
        available_times_for_date.append(times)

    return Response({
      'barber': barber.user.first_name,
      'date': date_str,
      'available_times': available_times_for_date
    })


# Edit Barber Schedule For Working
class EditBarberSchedule(generics.UpdateAPIView):
  queryset = Barber.objects.all()
  serializer_class = EditBarberScheduleSerializer
  permission_classes = [IsBarber]

  def get_object(self):
    user = self.request.user
    try:
      return Barber.objects.get(user=user)
    except Barber.DoesNotExist:
      raise NotFound('No barber has been found for this user.')