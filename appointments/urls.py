from django.urls import path
from appointments.views import CreateAppointment, DeleteAppointment, GetBarberAppointment, GetCustomerAppointment

urlpatterns = [
  path('create-appointment/', CreateAppointment.as_view()),
  path('get-barber-appointments/', GetBarberAppointment.as_view()),
  path('get-customer-appointments/', GetCustomerAppointment.as_view()),
  path('delete-appointment/<int:pk>/', DeleteAppointment.as_view()),
]