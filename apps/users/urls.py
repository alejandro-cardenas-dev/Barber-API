from django.urls import path
from apps.users.views.user_views import UserCreateView, UserDetailView

urlpatterns = [
  path('users/', UserCreateView.as_view(), name='create-account'),
  path('users/me/', UserDetailView.as_view(), name='user-detail'),
]
