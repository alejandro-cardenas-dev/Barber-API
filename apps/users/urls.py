from django.urls import path
from apps.users.views.create_user import CreateUserView
from apps.users.views.get_own_user import GetUser


urlpatterns = [
  path('users/', CreateUserView.as_view(), name='create-account'),
  path('users/me/', GetUser.as_view(), name='user-detail'),
]
