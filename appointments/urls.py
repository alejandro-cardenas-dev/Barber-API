from django.urls import path
from appointments.views import CreateAppointment, GetAppointment

urlpatterns = [
  path('create-appointment/', CreateAppointment.as_view()),
  path('get-appointment/', GetAppointment.as_view()),
]
