from django.urls import path

from customers.views import CreateCustomer, GetCustomers

urlpatterns = [
  path('get-customers/', GetCustomers.as_view()),
  path('create-customer/', CreateCustomer.as_view()),
]
