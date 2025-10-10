from django.urls import path

from appointments.views import CreateAppointment


urlpatterns = [
  path('create-appointment/', CreateAppointment.as_view()),
]
