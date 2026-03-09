from django.db import models

class Service(models.Model):
  name = models.CharField(max_length=100, unique=True)
  description = models.TextField(blank=False)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f'Service: {self.name}'