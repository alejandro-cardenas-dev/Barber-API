from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
  def has_permission(self, request, view):
    if not request.user or not request.user.is_authenticated:
      return False
    return getattr(request.user, "is_customer", False)

class IsBarber(BasePermission):
  def has_permission(self, request, view):
    if not request.user or not request.user.is_authenticated:
      return False
    return getattr(request.user, "is_barber", False)