from django.urls import path
from apps.users.views.create_user import CreateUserView
from apps.users.views.get_own_user import GetUser


urlpatterns = [
  path('create-account/', CreateUserView.as_view()),
  path('get-user/', GetUser.as_view()),
]
