from django.urls import path

from apps.barbers.views.barber_schedules import BarberScheduleListUpdateView
from apps.barbers.views.list import BarberListView
from apps.barbers.views.working_hours import BarberAvailabilityByDateView

urlpatterns = [
  path('barbers/', BarberListView.as_view(), name='barber-list'),
  path('barbers/me/schedule/', BarberScheduleListUpdateView.as_view(), name='barber-schedule'),
  path(
    'barbers/<int:barber_id>/available-times/',
    BarberAvailabilityByDateView.as_view(),
    name='barber-available-times'
  )
]
