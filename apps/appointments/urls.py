from django.urls import path
from apps.appointments.views.appointment_views import (
  AppointmentDeleteView,
  AppointmentListCreateView,
  CancelAppointmentView
)

urlpatterns = [
  path('appointments/', AppointmentListCreateView.as_view(), name='appointments-list'),
  path('appointments/<int:pk>/cancel/',CancelAppointmentView.as_view(), name='appointment-cancel'),
  path('appointments/<int:pk>/',AppointmentDeleteView.as_view(), name='appointment-delete'),
]