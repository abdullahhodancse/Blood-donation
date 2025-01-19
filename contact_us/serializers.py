from rest_framework import serializers
from . import models

class contact_us_serialaizers(serializers.ModelSerializer):
    class Meta:
        model=models.ContactUs
        fields='__all__'