from django.urls import path

from apps.barbers.views.barber_schedules import BarberScheduleView
from apps.barbers.views.list import GetBarber
from apps.barbers.views.working_hours import GetBarberAvailableTimesSpecificDate

urlpatterns = [
  path('barbers/', GetBarber.as_view(), name='barber-list'),
  path('barbers/me/schedule/', BarberScheduleView.as_view(), name='barber-schedule'),
  path(
    'barbers/<int:barber_id>/available-times/',
    GetBarberAvailableTimesSpecificDate.as_view(),
    name='barber-available-times'
  )
]
