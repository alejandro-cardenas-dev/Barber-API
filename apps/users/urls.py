from django.urls import path
from apps.users.views.create_user import UserCreateView
from apps.users.views.get_own_user import UserDetailView


urlpatterns = [
  path('users/', UserCreateView.as_view(), name='create-account'),
  path('users/me/', UserDetailView.as_view(), name='user-detail'),
]
