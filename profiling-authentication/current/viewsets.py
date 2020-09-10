from rest_framework.viewsets import ModelViewSet
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