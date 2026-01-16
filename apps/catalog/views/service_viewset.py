from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from apps.catalog.models import Service
from apps.catalog.serializers.create import ServiceCreateSerializer
from apps.catalog.serializers.read import ServiceReadSerializer
from rest_framework.response import Response
from rest_framework import status

class ServiceViewSet(ModelViewSet):
  queryset = Service.objects.filter(is_active=True)
  # permission_classes = [AllowAny]

  def get_serializer_class(self):
    if self.action in ('create', 'update', 'partial_update'):
      return ServiceCreateSerializer
    return ServiceReadSerializer

  def destroy(self, request, *args, **kwargs):
    service = self.get_object()
    service.is_active = False
    service.save(update_fields=['is_active'])
    return Response(
      {"detail": "Service deactivated successfully."},
      status=status.HTTP_204_NO_CONTENT
    )