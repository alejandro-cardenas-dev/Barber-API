from django.urls import path
from apps.appointments.views.delete import DeleteAppointment
from apps.appointments.views.list_create import AppointmentListCreateView

urlpatterns = [
  path('appointments/', AppointmentListCreateView.as_view(), name='appointments-list'),
  path('appointments/<int:pk>/',DeleteAppointment.as_view(), name='appointment-detail'),
]