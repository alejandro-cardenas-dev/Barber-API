from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
  """Only admin (is_staff) can perform the action."""

  def has_permission(self, request, view):
    if not request.user or not request.user.is_authenticated:
      return False
    return request.user.is_staff


class IsBarber(BasePermission):
  """Only barbers can perform the action."""

  def has_permission(self, request, view):
    if not request.user or not request.user.is_authenticated:
      return False
    return getattr(request.user, 'is_barber', False)


class IsCustomer(BasePermission):
  """Only customers can perform the action."""

  def has_permission(self, request, view):
    if not request.user or not request.user.is_authenticated:
      return False
    return getattr(request.user, 'is_customer', False)


class IsCustomerOrBarber(BasePermission):
  """Both customers and barbers can perform the action."""

  def has_permission(self, request, view):
    if not request.user or not request.user.is_authenticated:
      return False
    return request.user.is_customer or request.user.is_barber


class IsAppointmentOwner(BasePermission):
  """
  Only the owner of the appointment can perform the action.
  The owner is either the barber or the customer linked to the appointment.
  has_permission ensures the user is authenticated before object-level check.
  """

  def has_permission(self, request, view):
    return bool(request.user and request.user.is_authenticated)

  def has_object_permission(self, request, view, obj):
    return (
      obj.barber.user == request.user or
      obj.customer.user == request.user
    )