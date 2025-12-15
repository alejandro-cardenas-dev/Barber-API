from django.urls import path

from apps.barbers.views import BarberScheduleView, GetBarber, GetBarberAvailableTimesSpecificDate

urlpatterns = [
  path('get-barbers/', GetBarber.as_view()),
  path('edit-barber-schedule/', BarberScheduleView.as_view()),
  path('get-barber/<int:barber_id>/available-times/', GetBarberAvailableTimesSpecificDate.as_view()),
]
