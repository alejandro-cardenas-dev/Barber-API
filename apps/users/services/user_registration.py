from django.db import transaction
from apps.barbers.models import Barber
from apps.customers.models import Customer
from apps.users.models import User

@transaction.atomic
def register_user(
    *,
    email,
    password,
    first_name,
    last_name,
    phone,
    is_barber,
    is_customer
):

  user = User.objects.create_user(
    email=email,
    password=password,
    first_name=first_name,
    last_name=last_name,
    phone=phone,
    is_barber=is_barber,
    is_customer=is_customer
  )

  if is_barber:
    Barber.objects.create(user=user)
  else:
    Customer.objects.create(user=user)

  return user