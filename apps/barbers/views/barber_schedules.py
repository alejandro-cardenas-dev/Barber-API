from rest_framework.exceptions import NotFound
from rest_framework import generics
from apps.barbers.models import Barber
from apps.barbers.serializers.edit import EditBarberScheduleSerializer
from permissions import IsBarber

# Get and Update Barber Schedule
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
    user = self.request.user
    try:
      return Barber.objects.get(user=user)
    except Barber.DoesNotExist:
      raise NotFound("No barber has been found for this user.")