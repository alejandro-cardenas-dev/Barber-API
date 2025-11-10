from django.urls import path

from users.views import CreateUserView, GetUser

urlpatterns = [
  path('create-account/', CreateUserView.as_view()),
  path('get-user/', GetUser.as_view()),
]
