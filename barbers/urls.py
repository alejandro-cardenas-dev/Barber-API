from django.urls import path

from barbers.views import EditBarberSchedule, GetBarber

urlpatterns = [
  path('get-barbers/', GetBarber.as_view()),
  path('edit-barber-schedule/', EditBarberSchedule.as_view())
]
