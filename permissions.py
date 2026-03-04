from rest_framework.permissions import BasePermission


# Only the owner can perform the action.
class IsAppointmentOwner(BasePermission):
  def has_object_permission(self, request, view, obj):
    return obj.barber.user == request.user or obj.customer.user == request.user


# Only the customer can perform the action
class IsCustomer(BasePermission):
  def has_permission(self, request, view):
    if not request.user or not request.user.is_authenticated:
      return False
    return getattr(request.user, "is_customer", False)


# Only the barber can perform the action
class IsBarber(BasePermission):
  def has_permission(self, request, view):
    if not request.user or not request.user.is_authenticated:
      return False
    return getattr(request.user, "is_barber", False)

# Both barber or customer can perfome the action
class IsCustomerOrBarber(BasePermission):
  def has_permission(self, request, view):
    if not request.user or not request.user.is_authenticated:
      return False
    return request.user.is_customer or request.user.is_barber