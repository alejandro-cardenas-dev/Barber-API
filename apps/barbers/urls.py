from django.urls import path
from apps.barbers.views.barber_views import (
  BarberAvailabilityByDateView,
  BarberDetailAdminView,
  BarberListView,
  BarberScheduleListUpdateView
)

urlpatterns = [
  path('barbers/', BarberListView.as_view(), name='barber-list'),
  path('barbers/<int:pk>/', BarberDetailAdminView.as_view(), name='barber-detail'),
  path('barbers/me/schedule/', BarberScheduleListUpdateView.as_view(), name='barber-schedule'),
  path(
    'barbers/<int:barber_id>/available-times/',
    BarberAvailabilityByDateView.as_view(),
    name='barber-available-times'
  ),
]