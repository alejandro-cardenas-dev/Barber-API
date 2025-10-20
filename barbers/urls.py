from django.urls import path

from barbers.views import EditBarberSchedule, GetBarber, GetBarberAvailableTimesSpecificDate

urlpatterns = [
  path('get-barbers/', GetBarber.as_view()),
  path('edit-barber-schedule/', EditBarberSchedule.as_view()),
  path('get-barber/<int:barber_id>/available-times/', GetBarberAvailableTimesSpecificDate.as_view()),
]
