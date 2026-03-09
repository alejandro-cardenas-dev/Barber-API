from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.catalog.models import Service
from apps.catalog.serializers.catalog_serializers import ServiceCreateSerializer, ServiceReadSerializer

from permissions import IsAdmin

class ServiceViewSet(ModelViewSet):

  def get_queryset(self):
    if self.request.user.is_staff:
      return Service.objects.all()
    return Service.objects.filter(is_active=True)

  def get_serializer_class(self):
    if self.action in ('create', 'update', 'partial_update'):
      return ServiceCreateSerializer
    return ServiceReadSerializer

  def get_permissions(self):
    if self.action in ('list', 'retrieve'):
      return [AllowAny()]
    return [IsAdmin()]

  def destroy(self, request, *args, **kwargs):
    service = self.get_object()
    service.is_active = False
    service.save(update_fields=['is_active'])
    return Response(
      {"detail": "Service deactivated successfully."},
      status=status.HTTP_204_NO_CONTENT
    )