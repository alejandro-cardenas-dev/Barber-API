from django.core.management.base import BaseCommand
from apps.users.models import User


class Command(BaseCommand):
  help = 'Creates a default admin user if none exists'

  def handle(self, *args, **kwargs):
    if not User.objects.filter(is_staff=True).exists():
      User.objects.create_superuser(
        email='admin@barbershop.com',
        password='temporal123'
      )
      self.stdout.write(self.style.SUCCESS('Admin created successfully'))
    else:
      self.stdout.write('Admin already exists, skipping.')