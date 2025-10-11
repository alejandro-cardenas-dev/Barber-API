from django.urls import path

from barbers.views import GetBarber

urlpatterns = [
  path('get-barbers/', GetBarber.as_view()),
]
