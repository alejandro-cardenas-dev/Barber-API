from django.urls import path

from barbers.views import CreateBarber, ShowBarber

urlpatterns = [
  path('get-barbers/', ShowBarber.as_view()),
  path('create-barber/', CreateBarber.as_view()),
]
