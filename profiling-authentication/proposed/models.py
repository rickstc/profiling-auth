from django.db import models
from django.contrib.postgres.fields import ArrayField
from profiling_authentication.models import UUIDPKModel

class Role(UUIDPKModel):
    name = models.CharField(max_length=32, blank=False)
    description = models.CharField(max_length=128, blank=False)
    is_inheritable = models.BooleanField(blank=False, default=False)
    permissions = ArrayField(
        models.CharField(max_length=32, blank = False, unique=True),
        null=False,
        blank=True,
        default = list
    )

    def has_permission(self, permission_slug):
        """ Checks to see if the permission object is in the role """
        if permission_slug in self.permissions:
            return True
        return False

class Profile(UUIDPKModel):
    first_name = models.CharField(max_length=32, blank=False)
    roles = models.ManyToManyField(Role, related_name='roles', blank=True)
    permissions = ArrayField(
        models.CharField(max_length=32, blank = False, unique=True),
        null=False,
        blank=True,
        default = list
    )

    def has_permission(self, permission_slug):
        """ Checks the permission """

        if permission_slug in self.permissions:
            return True

        for role in self.roles.all():
            if role.has_permission(permission_slug):
                return True

        return False