from django.urls import path

from barbers.views import CreateBarber, GetBarber

urlpatterns = [
  path('get-barbers/', GetBarber.as_view()),
  path('create-barber/', CreateBarber.as_view()),
]
