from rest_framework import serializers
from . import models

class ServicesSerialaizers(serializers.ModelSerializer):
    class Meta:
        model=models.service
        fields='__all__'