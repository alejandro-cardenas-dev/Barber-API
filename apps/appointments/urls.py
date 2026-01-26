from django.urls import path
from apps.appointments.views.delete import AppointmentDeleteView
from apps.appointments.views.list_create import AppointmentListCreateView

urlpatterns = [
  path('appointments/', AppointmentListCreateView.as_view(), name='appointments-list'),
  path('appointments/<int:pk>/',AppointmentDeleteView.as_view(), name='appointment-detail'),
]