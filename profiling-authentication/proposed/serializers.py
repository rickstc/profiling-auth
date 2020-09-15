from rest_framework import serializers
from proposed import models

class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(
        child = serializers.CharField(max_length=32),
        required=False,
        allow_empty=True
    )
    class Meta:
        model = models.Role
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):

    permissions = serializers.ListField(
        child = serializers.CharField(max_length=32),
        required=False,
        allow_empty=True
    )


    class Meta:
        model = models.Profile
        fields = '__all__'