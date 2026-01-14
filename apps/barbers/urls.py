from django.urls import path

from apps.barbers.views.barber_schedules import BarberScheduleView
from apps.barbers.views.list import GetBarber
from apps.barbers.views.working_hours import GetBarberAvailableTimesSpecificDate

urlpatterns = [
  path('get-barbers/', GetBarber.as_view()),
  path('edit-barber-schedule/', BarberScheduleView.as_view()),
  path('get-barber/<int:barber_id>/available-times/', GetBarberAvailableTimesSpecificDate.as_view()),
]
