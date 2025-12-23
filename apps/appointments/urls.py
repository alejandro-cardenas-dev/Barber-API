from django.urls import path
from apps.appointments.views.create import CreateAppointment
from apps.appointments.views.list import GetAppointment
from apps.appointments.views.delete import DeleteAppointment

urlpatterns = [
  path('create-appointment/', CreateAppointment.as_view()),
  path('get-appointments/', GetAppointment.as_view()),
  path('delete-appointment/<int:pk>/', DeleteAppointment.as_view()),
]