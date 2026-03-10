import os
from django.core.management.base import BaseCommand
from apps.users.models import User


class Command(BaseCommand):
  help = 'Creates or updates the default admin user'

  def handle(self, *args, **kwargs):
    email = os.environ.get('ADMIN_EMAIL', 'admin@barbershop.com')
    password = os.environ.get('ADMIN_PASSWORD', 'temporal123')

    user, created = User.objects.get_or_create(
      is_staff=True,
      defaults={'email': email}
    )
    user.set_password(password)
    user.save()

    if created:
      self.stdout.write(self.style.SUCCESS('Admin created successfully'))
    else:
      self.stdout.write(self.style.SUCCESS('Admin password updated successfully'))