from django.db import models
import uuid

class UUIDPKModel(models.Model):
    """ Replaces standard numerical primary key with a UUID-based primary key """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
