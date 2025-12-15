from django.urls import path
from apps.appointments.views import CreateAppointment, DeleteAppointment, GetAppointment

urlpatterns = [
  path('create-appointment/', CreateAppointment.as_view()),
  path('get-appointments/', GetAppointment.as_view()),
  path('delete-appointment/<int:pk>/', DeleteAppointment.as_view()),
]