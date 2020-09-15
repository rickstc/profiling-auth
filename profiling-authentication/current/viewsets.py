from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from current import models
from current import serializers


class PermissionViewSet(ModelViewSet):

    queryset = models.Permission.objects.all()
    serializer_class = serializers.PermissionSerializer

class RoleViewSet(ModelViewSet):

    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer

class ProfileViewSet(ModelViewSet):

    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    @action(detail=True, methods=['post'])
    def check(self, request, pk=None):
        profile = self.get_object()
        permission_slug = self.request.data.get('permission_slug', None)
        if permission_slug is None:
            return Response({"message": "permission_slug must be present"}, status.HTTP_400_BAD_REQUEST)
        if profile.has_permission(permission_slug):
            return Response({"message": "permission existed"}, status=status.HTTP_200_OK)
        return Response({"message": "permission did not exist"}, status=status.HTTP_403_FORBIDDEN)

    