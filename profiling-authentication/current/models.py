from django.db import models
from profiling_authentication.models import UUIDPKModel

class Permission(UUIDPKModel):
    slug = models.CharField(blank = False, max_length = 32, unique=True)
    name = models.CharField(blank = False, max_length = 64)
    description = models.TextField(default = "")
    is_system = models.BooleanField(default=False, null=False)

class Role(UUIDPKModel):
    name = models.CharField(max_length=32, blank=False)
    description = models.CharField(max_length=128, blank=False)
    is_inheritable = models.BooleanField(blank=False, default=False)
    permissions = models.ManyToManyField(Permission, related_name='role_permissions', blank=True)

    def has_permission(self, permission_object):
        """ Checks to see if the permission object is in the role """
        if permission_object in self.permissions.all():
            return True
        return False

class Profile(UUIDPKModel):
    first_name = models.CharField(max_length=32, blank=False)
    roles = models.ManyToManyField(Role, related_name='roles', blank=True)
    permissions = models.ManyToManyField(Permission, related_name='profile_permissions', blank=True)

    def has_permission(self, permission_slug):
        """ Checks the permission """
        try:
            permission = Permission.objects.get(slug=permission_slug)
        except Permission.DoesNotExist:
            print(f"This permission did not exist: {permission_slug}")
            return False

        if permission in self.permissions.all():
            return True

        for role in self.roles.all():
            if role.has_permission(permission):
                return True

        return False
    